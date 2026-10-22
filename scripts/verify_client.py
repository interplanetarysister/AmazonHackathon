"""Check the actual inline browser JavaScript without additional npm dependencies.

Run: python scripts/verify_client.py
Requires a Node.js executable for syntax checking; exits nonzero when Node
is unavailable so this cannot be accidentally reported as a passing test.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


class InlineScriptCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_script = False
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.in_script = not any(k == "src" for k, _ in attrs)
            if self.in_script:
                self.scripts.append("")

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False

    def handle_data(self, data):
        if self.in_script:
            self.scripts[-1] += data


def main() -> int:
    node = shutil.which("node")
    if not node:
        print("NOT VERIFIED: Node.js is unavailable; install/use an existing Node 20+ runtime.")
        return 2
    source = Path(__file__).resolve().parents[1] / "web" / "index.html"
    parser = InlineScriptCollector()
    parser.feed(source.read_text(encoding="utf-8"))
    if not parser.scripts:
        print("FAIL: no inline client script was found.")
        return 1
    with tempfile.TemporaryDirectory() as directory:
        for i, script in enumerate(parser.scripts, start=1):
            js_path = Path(directory) / f"browser-{i}.js"
            js_path.write_text(script, encoding="utf-8")
            result = subprocess.run([node, "--check", str(js_path)], text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    check=False, timeout=20)
            if result.returncode:
                print("FAIL: inline script", i)
                print(result.stderr.strip())
                return 1
    for external in ("v2.js", "notify-sw.js", "judge.js"):
        file_path = source.parent / external
        result = subprocess.run([node, "--check", str(file_path)], text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                check=False, timeout=20)
        if result.returncode:
            print("FAIL: external script", external)
            print(result.stderr.strip())
            return 1
    print(f"PASS: {len(parser.scripts)} inline script(s) and 3 external scripts parsed by Node.js.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
