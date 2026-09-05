#!/usr/bin/env python3
"""Bounded Chrome viewport captures. Python 3.9+, Linux/macOS, no pip dependencies."""

from __future__ import annotations

import argparse
import csv
import functools
import hashlib
import http.server
import json
import os
from pathlib import Path
import re
import shutil
import signal
import struct
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

MATRICES = {
    "quick": "390x844 844x390 1440x900 2560x1440",
    "standard": "390x844 844x390 820x1180 1180x820 1440x1000 1000x1440 2560x1440 1440x2560 2560x1080 1080x2560",
    "comprehensive": "320x568 568x320 360x800 800x360 390x844 844x390 412x915 915x412 "
    "768x1024 1024x768 820x1180 1180x820 1024x1366 1366x1024 "
    "1280x720 720x1280 1366x768 768x1366 1440x900 900x1440 "
    "1920x1080 1080x1920 2560x1440 1440x2560 3440x1440 1440x3440 3840x2160 2160x3840",
}


def component(value: str) -> str:
    if value in {".", ".."} or not re.fullmatch(r"[A-Za-z0-9._-]+", value):
        raise argparse.ArgumentTypeError("use a filename component, excluding . and ..")
    return value


def positive(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, type=component)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url")
    source.add_argument("--directory", type=Path)
    parser.add_argument("--output", type=Path, help="evidence root; default: system temporary directory")
    parser.add_argument("--phase", default="capture", type=component)
    parser.add_argument("--matrix", choices=MATRICES, default="standard")
    parser.add_argument("--viewport", action="append", help="WIDTHxHEIGHT; repeatable, overrides matrix")
    parser.add_argument("--port", type=int, default=0, help="static server port; default: automatically assigned")
    parser.add_argument("--browser", help="Chrome/Chromium executable name or path")
    parser.add_argument("--timeout", type=positive, default=30, help="seconds per browser or montage operation")
    parser.add_argument("--ready-timeout", type=positive, default=10, help="seconds to wait for HTTP readiness")
    parser.add_argument("--motion", choices=("reduce", "browser-default"), default="reduce")
    parser.add_argument("--no-contact-sheet", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("--port must be 0 through 65535")
    if args.directory and not args.directory.is_dir():
        parser.error("--directory must exist")
    if args.url:
        parsed = urllib.parse.urlsplit(args.url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or any(ord(c) < 32 for c in args.url):
            parser.error("--url must be an HTTP(S) URL without control characters")
        if parsed.username is not None or parsed.password is not None:
            parser.error("credentials in --url are unsupported; use a repository-native authenticated harness")
    args.viewports = list(dict.fromkeys(args.viewport or MATRICES[args.matrix].split()))
    for viewport in args.viewports:
        if not re.fullmatch(r"[1-9][0-9]{2,4}x[1-9][0-9]{2,4}", viewport):
            parser.error(f"invalid viewport: {viewport}")
    candidates = [args.browser] if args.browser else [
        "chromium", "chromium-browser", "google-chrome-stable", "google-chrome", "chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    args.browser = next((shutil.which(item) for item in candidates if shutil.which(item)), None)
    if not args.browser:
        parser.error("Chrome/Chromium not found; pass --browser")
    return args


def run(command: list[str], timeout: int, log: Path) -> None:
    """Terminate only this invocation's process group, including browser children."""
    with log.open("wb") as stream:
        process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            code = process.wait(timeout=timeout)
            if code:
                raise RuntimeError(f"command exited {code}; see {log.name}")
        finally:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()


def wait_http(url: str, seconds: int) -> dict:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=min(2, max(.01, deadline - time.monotonic()))) as response:
                return {"url": response.url, "status": response.status}
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(min(.2, max(0, deadline - time.monotonic())))
    raise RuntimeError("HTTP readiness timed out; this check does not establish application readiness")


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as stream:
        header = stream.read(24)
        stream.seek(-12, os.SEEK_END)
        end = stream.read()
    if header[:16] != b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" or end != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        raise RuntimeError(f"invalid or incomplete PNG: {path.name}")
    return struct.unpack(">II", header[16:24])


def capture(args: argparse.Namespace, evidence: Path, receipt: dict) -> None:
    server = None
    server_log = None
    try:
        if args.directory:
            server_log = (evidence / "server.log").open("w")

            class Handler(http.server.SimpleHTTPRequestHandler):
                def log_message(self, fmt, *values):
                    server_log.write((fmt % values) + "\n")
                    server_log.flush()

            class Server(http.server.ThreadingHTTPServer):
                def handle_error(self, request, client_address):
                    traceback.print_exc(file=server_log)

            handler = functools.partial(Handler, directory=str(args.directory.resolve()))
            # Binding here proves ownership. An occupied explicit port fails before capture.
            server = Server(("127.0.0.1", args.port), handler)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            args.url = f"http://127.0.0.1:{server.server_port}/"
        receipt["url"] = args.url
        receipt["http_probe"] = wait_http(args.url, args.ready_timeout)
        run([args.browser, "--version"], args.timeout, evidence / "browser-version.log")
        receipt["browser_version"] = (evidence / "browser-version.log").read_text(errors="replace").strip()
        with (evidence / "receipt.tsv").open("w", newline="") as stream:
            writer = csv.writer(stream, delimiter="\t")
            writer.writerow(["viewport", "width", "height", "bytes", "sha256", "url"])
            for viewport in args.viewports:
                receipt["active_viewport"] = viewport
                width, height = map(int, viewport.split("x"))
                screenshot = evidence / f"{viewport}.png"
                with tempfile.TemporaryDirectory(prefix="capture-profile-") as profile:
                    command = [args.browser, "--headless", "--no-first-run", "--no-default-browser-check",
                               f"--user-data-dir={profile}", "--force-device-scale-factor=1",
                               f"--window-size={width},{height}", f"--screenshot={screenshot}"]
                    if args.motion == "reduce":
                        command.append("--force-prefers-reduced-motion")
                    command.append(args.url)
                    run(command, args.timeout, evidence / f"{viewport}.browser.log")
                actual = png_size(screenshot)
                if actual != (width, height):
                    raise RuntimeError(f"{viewport} produced {actual[0]}x{actual[1]} pixels")
                data = screenshot.read_bytes()
                record = {"viewport": viewport, "width": width, "height": height,
                          "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "path": screenshot.name}
                receipt["captures"].append(record)
                writer.writerow([viewport, width, height, record["bytes"], record["sha256"], args.url])
                stream.flush()
        receipt.pop("active_viewport", None)
        receipt["contact_sheet"] = {"status": "skipped"}
        montage = [shutil.which("magick"), "montage"] if shutil.which("magick") else [shutil.which("montage")]
        if not args.no_contact_sheet and montage[0]:
            command = montage + ["-background", "#20242b", "-fill", "white"]
            for item in receipt["captures"]:
                command.extend(["-label", item["viewport"], str(evidence / item["path"])])
            command.extend(["-thumbnail", "520x520>", "-tile", "2x", "-geometry", "+16+24",
                            str(evidence / "contact-sheet.png")])
            try:
                run(command, args.timeout, evidence / "contact-sheet.log")
                png_size(evidence / "contact-sheet.png")
                receipt["contact_sheet"] = {"status": "complete", "path": "contact-sheet.png"}
            except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
                receipt["contact_sheet"] = {"status": "failed", "error": str(error)}
                print("Contact sheet failed; original captures remain available.", file=sys.stderr)
        receipt["status"] = "complete"
    finally:
        if server:
            server.shutdown()
            server.server_close()
        if server_log:
            server_log.close()


def main() -> int:
    args = arguments()
    if os.name != "posix":
        raise SystemExit("This runner requires Linux/macOS process groups")
    root = args.output or Path(tempfile.gettempdir()) / "visual-evidence"
    parent = root.expanduser().resolve() / args.phase / args.name
    parent.mkdir(parents=True, exist_ok=True)
    evidence = Path(tempfile.mkdtemp(prefix="run-", dir=parent))
    receipt = {"schema_version": 1, "status": "incomplete", "started_at": datetime.now(timezone.utc).isoformat(),
               "browser": args.browser, "viewports": args.viewports, "matrix": "custom" if args.viewport else args.matrix,
               "motion_requested": args.motion, "device_scale_factor_requested": 1,
               "coverage": "initial viewport only", "application_readiness": "not asserted",
               "captures": [], "timeout_seconds": args.timeout}
    code = 1
    def interrupted(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, interrupted)
    try:
        capture(args, evidence, receipt)
        code = 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, KeyboardInterrupt) as error:
        receipt["error"] = str(error) or "interrupted"
        print(f"Capture incomplete: {receipt['error']}", file=sys.stderr)
    finally:
        (evidence / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(f"Evidence: {evidence}\nReceipt: {evidence / 'receipt.json'}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
