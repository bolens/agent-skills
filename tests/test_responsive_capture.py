from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/responsive-web-capture/scripts/capture-responsive.sh"
FAKE_BROWSER = '''#!/usr/bin/env python3
import os, struct, sys, time, zlib
from pathlib import Path
if "--version" in sys.argv:
    print("Fixture Browser 1")
    sys.exit(0)
mode = os.environ.get("CAPTURE_FIXTURE", "success")
if mode == "hang":
    Path(os.environ["CAPTURE_MARKER"]).write_text("running")
    time.sleep(60)
if mode == "missing":
    sys.exit(0)
size = next(x.split("=", 1)[1] for x in sys.argv if x.startswith("--window-size="))
w, h = map(int, size.split(","))
if mode == "wrong-size":
    w += 1
path = Path(next(x.split("=", 1)[1] for x in sys.argv if x.startswith("--screenshot=")))
def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
png = b"\\x89PNG\\r\\n\\x1a\\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w,h,8,2,0,0,0))
png += chunk(b"IDAT", zlib.compress((b"\\0" + b"\\x80" * (w * 3)) * h)) + chunk(b"IEND", b"")
path.write_bytes(png)
'''


@unittest.skipUnless(os.name == "posix", "runner requires POSIX process groups")
class ResponsiveCapture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.site = self.root / "site"
        self.site.mkdir()
        (self.site / "index.html").write_text("<h1>Capture fixture</h1>")
        self.browser = self.root / "fake-browser"
        self.browser.write_text(FAKE_BROWSER)
        self.browser.chmod(0o755)

    def capture(self, *options, mode="success"):
        return subprocess.run([
            "bash", str(SCRIPT), "--name", "fixture", "--directory", str(self.site),
            "--browser", str(self.browser), "--output", str(self.root / "evidence"),
            "--viewport", "320x568", "--no-contact-sheet", *options,
        ], capture_output=True, text=True, timeout=10,
            env={**os.environ, "CAPTURE_FIXTURE": mode, "CAPTURE_MARKER": str(self.root / "running")})

    def receipts(self):
        return list((self.root / "evidence").rglob("receipt.json"))

    def test_successful_reruns_preserve_evidence_and_deduplicate_viewports(self):
        first = self.capture("--viewport", "320x568", "--motion", "browser-default")
        self.assertEqual(0, first.returncode, first.stderr)
        original = self.receipts()[0]
        saved = original.read_bytes()
        second = self.capture()
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual(2, len(self.receipts()))
        self.assertEqual(saved, original.read_bytes())
        receipt = json.loads(saved)
        self.assertEqual("complete", receipt["status"])
        self.assertEqual(1, len(receipt["captures"]))
        self.assertEqual("browser-default", receipt["motion_requested"])
        self.assertEqual("skipped", receipt["contact_sheet"]["status"])
        self.assertEqual("Fixture Browser 1", receipt["browser_version"])

    def test_missing_or_wrong_size_image_never_reports_complete(self):
        for mode in ("missing", "wrong-size"):
            with self.subTest(mode=mode):
                result = self.capture(mode=mode)
                self.assertNotEqual(0, result.returncode)
        for path in self.receipts():
            receipt = json.loads(path.read_text())
            self.assertEqual("incomplete", receipt["status"])
            self.assertEqual([], receipt["captures"])
            self.assertEqual("320x568", receipt["active_viewport"])

    def test_hung_browser_is_bounded_and_leaves_failure_receipt(self):
        result = self.capture("--timeout", "1", mode="hang")
        self.assertNotEqual(0, result.returncode)
        receipt = json.loads(self.receipts()[0].read_text())
        self.assertEqual("incomplete", receipt["status"])
        self.assertIn("timed out", receipt["error"])

    def test_occupied_static_port_fails_instead_of_capturing_other_site(self):
        with socket.socket() as occupied:
            occupied.bind(("127.0.0.1", 0))
            occupied.listen()
            result = self.capture("--port", str(occupied.getsockname()[1]))
        self.assertNotEqual(0, result.returncode)
        receipt = json.loads(self.receipts()[0].read_text())
        self.assertEqual("incomplete", receipt["status"])
        self.assertEqual([], receipt["captures"])

    def test_interruption_preserves_receipt_and_stops_owned_server(self):
        marker = self.root / "running"
        process = subprocess.Popen([
            "bash", str(SCRIPT), "--name", "fixture", "--directory", str(self.site),
            "--browser", str(self.browser), "--output", str(self.root / "evidence"),
            "--viewport", "320x568", "--no-contact-sheet",
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            env={**os.environ, "CAPTURE_FIXTURE": "hang", "CAPTURE_MARKER": str(marker)})
        try:
            deadline = time.monotonic() + 5
            while not marker.exists() and process.poll() is None and time.monotonic() < deadline:
                time.sleep(.02)
            self.assertTrue(marker.exists(), "browser did not start")
            process.terminate()
            process.communicate(timeout=5)
            self.assertNotEqual(0, process.returncode)
            receipt = json.loads(self.receipts()[0].read_text())
            self.assertEqual("incomplete", receipt["status"])
            self.assertEqual("interrupted", receipt["error"])
            port = int(receipt["url"].rstrip("/").rsplit(":", 1)[1])
            with socket.socket() as probe:
                probe.settimeout(1)
                self.assertNotEqual(0, probe.connect_ex(("127.0.0.1", port)))
        finally:
            if process.poll() is None:
                process.terminate()
            process.communicate(timeout=5)

    def test_invalid_arguments_do_not_create_evidence(self):
        for options in (("--phase", ".."), ("--viewport", "oops"), ("--timeout", "0"), ("--port",)):
            with self.subTest(options=options):
                self.assertEqual(2, self.capture(*options).returncode)
        self.assertEqual([], self.receipts())


if __name__ == "__main__":
    unittest.main()
