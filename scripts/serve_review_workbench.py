"""Loopback-only static preview with byte-range support for replay frame seeking."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re


class ReplayHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.remaining = None
        path = Path(self.translate_path(self.path))
        header = self.headers.get("Range")
        if not header or path.suffix != ".mp4" or not path.is_file():
            return super().send_head()
        size = path.stat().st_size
        match = re.fullmatch(r"bytes=(\d+)-(\d*)", header)
        if match:
            start = int(match[1])
            end = min(int(match[2]) if match[2] else size - 1, size - 1)
        if not match or not 0 <= start <= end < size:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None
        stream = path.open("rb")
        stream.seek(start)
        self.remaining = end - start + 1
        self.send_response(206)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(self.remaining))
        self.end_headers()
        return stream

    def copyfile(self, source, output):
        if self.remaining is None:
            return super().copyfile(source, output)
        while self.remaining:
            chunk = source.read(min(self.remaining, 65536))
            if not chunk:
                break
            output.write(chunk)
            self.remaining -= len(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--port", type=int, default=8088)
    args = parser.parse_args()
    if not (args.directory / "reuse_manifest.json").is_file():
        parser.error("Choose a generated review-workbench folder")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(
        ReplayHandler, directory=str(args.directory.resolve())))
    print(f"Open http://127.0.0.1:{args.port}/", flush=True)
    server.serve_forever()
