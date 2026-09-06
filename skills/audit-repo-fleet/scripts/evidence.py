#!/usr/bin/env python3
"""Run native checks with bounded execution and worktree-local evidence."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import tempfile
import time
import uuid


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def repository(path):
    return Path(os.fsdecode(git(path, "rev-parse", "--show-toplevel")).strip()).resolve()


def fingerprint(root):
    """Hash source and index identity, never source contents into the receipt."""
    digest = hashlib.sha256()
    head = git(root, "rev-parse", "HEAD").decode().strip()
    digest.update(head.encode())
    branch = subprocess.run(["git", "-C", str(root), "symbolic-ref", "--quiet", "HEAD"], capture_output=True, check=False).stdout
    digest.update(branch)
    digest.update(git(root, "ls-files", "--stage", "-z"))
    names = sorted(set(git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z").split(b"\0")) - {b""})
    for name in names:
        digest.update(len(name).to_bytes(8, "big"))
        digest.update(name)
        path = root / os.fsdecode(name)
        # A replaced parent directory must not cause reads outside the checkout.
        parent_link = next((p for p in path.parents if p != root and root in p.parents and p.is_symlink()), None)
        if parent_link:
            digest.update(b"parent-symlink\0" + os.fsencode(os.readlink(parent_link)))
            continue
        try:
            before = path.lstat()
        except FileNotFoundError:
            digest.update(b"missing\0")
            continue
        if stat.S_ISLNK(before.st_mode):
            digest.update(b"symlink\0" + os.fsencode(os.readlink(path)))
        elif stat.S_ISREG(before.st_mode):
            digest.update(b"file\0" + str(before.st_mode & 0o111).encode() + b"\0" + str(before.st_size).encode() + b"\0")
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
            after = path.lstat()
            if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
                raise RuntimeError("Source changed while fingerprinting; retry after the writer finishes")
        else:
            raise RuntimeError("Unsupported source file type: " + os.fsdecode(name))
        digest.update(b"\0end\0")
    return {"head": head, "sha256": digest.hexdigest()}


def storage(root):
    path = Path(os.fsdecode(git(root, "rev-parse", "--absolute-git-dir")).strip()) / "fleet-evidence"
    path.mkdir(mode=0o700, exist_ok=True)
    if path.is_symlink():
        raise RuntimeError("Evidence directory must not be a symlink")
    return path


def save(path, record):
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        temp = Path(stream.name)
        json.dump(record, stream, indent=2)
        stream.write("\n")
    os.replace(temp, path)


def records(directory):
    for path in directory.glob("*/result.json"):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(record, dict) or not all(key in record for key in ("id", "label", "command", "candidate", "status", "started")):
                raise ValueError("missing receipt fields")
        except (OSError, ValueError) as exc:
            raise RuntimeError("Unreadable evidence receipt: " + str(path)) from exc
        yield record


def stop_process(process):
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    elif os.name == "nt":
        taskkill = Path(os.environ.get("SystemRoot", "C:/Windows")) / "System32/taskkill.exe"
        subprocess.run([str(taskkill), "/PID", str(process.pid), "/T", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    if process.poll() is None:
        process.kill()
    process.wait()


def execute(args):
    root = repository(args.repo)
    before = fingerprint(root)
    directory = storage(root)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        raise ValueError("Supply a native check command after --")
    # Reserve an unchanged command/candidate before counting attempts. Different
    # checks may run concurrently, but identical retries must not race the cap.
    lock_key = hashlib.sha256(json.dumps([before, command], sort_keys=True).encode()).hexdigest()
    lock = directory / (lock_key + ".lock")
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise RuntimeError("This candidate and command already have a run lock: " + str(lock)) from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "started": time.time()}, stream)
        return execute_locked(args, root, before, directory, command)
    finally:
        lock.unlink()


def execute_locked(args, root, before, directory, command):
    failures = [r for r in records(directory) if r.get("candidate") == before and r.get("command") == command and r.get("status") in {"failed", "timed_out", "interrupted", "unavailable"}]
    if len(failures) >= args.max_attempts:
        raise ValueError("Attempt limit reached for this unchanged candidate and command")
    if failures and not args.retry_reason:
        raise ValueError("Diagnose the previous failure; an unchanged retry requires --retry-reason")
    run_id = str(uuid.uuid4())
    run_dir = directory / run_id
    run_dir.mkdir(mode=0o700)
    record = {"version": 1, "id": run_id, "label": args.label, "command": command,
              "candidate": before, "status": "running", "started": time.time(),
              "timeout_seconds": args.timeout, "attempt": len(failures) + 1,
              "retry_reason": args.retry_reason, "stdout": str(run_dir / "stdout.log"),
              "stderr": str(run_dir / "stderr.log")}
    receipt = run_dir / "result.json"
    save(receipt, record)
    start = time.monotonic()
    process = None
    code = 1
    with (run_dir / "stdout.log").open("xb") as out, (run_dir / "stderr.log").open("xb") as err:
        os.chmod(out.name, 0o600)
        os.chmod(err.name, 0o600)
        try:
            process = subprocess.Popen(command, cwd=root, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                       start_new_session=os.name == "posix")
            record["pid"] = process.pid
            save(receipt, record)
            code = process.wait(timeout=args.timeout)
            record["status"] = "passed" if code == 0 else "failed"
        except FileNotFoundError as exc:
            record["status"] = "unavailable"
            err.write(str(exc).encode())
            code = 127
        except subprocess.TimeoutExpired:
            stop_process(process)
            record["status"] = "timed_out"
            code = 124
        except KeyboardInterrupt:
            if process:
                stop_process(process)
            record["status"] = "interrupted"
            code = 130
        except OSError as exc:
            record["status"] = "unavailable"
            err.write(str(exc).encode())
            code = 126
    record["exit_code"] = code
    record["elapsed_seconds"] = round(time.monotonic() - start, 3)
    try:
        after = fingerprint(root)
        record["candidate_after"] = after
        if after != before and code == 0:
            record["status"] = "changed"
            code = 125
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        record["status"] = "unverified"
        record["verification_error"] = str(exc)
        code = 125
    save(receipt, record)
    print(json.dumps({"status": record["status"], "receipt": str(receipt), "exit_code": record["exit_code"]}))
    return code if 0 <= code <= 255 else 1


def report(args):
    root = repository(args.repo)
    current = fingerprint(root)
    items = sorted(records(storage(root)), key=lambda r: r.get("started", 0))
    result = []
    for label in args.label:
        matching = [r for r in items if r.get("label") == label]
        if not matching:
            result.append({"label": label, "status": "missing"})
            continue
        record = matching[-1]
        status = record["status"]
        if record.get("candidate") != current:
            status = "stale"
        result.append({"label": label, "status": status, "id": record["id"], "command": record["command"]})
    print(json.dumps(result, indent=2))
    return 0 if result and all(r["status"] == "passed" for r in result) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    sub = parser.add_subparsers(dest="operation", required=True)
    run = sub.add_parser("run")
    run.add_argument("--label", required=True)
    run.add_argument("--timeout", type=float, default=900)
    run.add_argument("--max-attempts", type=int, default=3)
    run.add_argument("--retry-reason")
    run.add_argument("command", nargs=argparse.REMAINDER)
    show = sub.add_parser("report")
    show.add_argument("--label", action="append", required=True)
    args = parser.parse_args(argv)
    if args.operation == "run" and (not 0 < args.timeout <= 86400 or not 1 <= args.max_attempts <= 10):
        parser.error("timeout must be 0–86400 seconds (exclusive zero); max-attempts must be 1–10")
    try:
        return execute(args) if args.operation == "run" else report(args)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
