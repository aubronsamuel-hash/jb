"""Simple WSGI server used to expose the Orga dashboard API."""
from __future__ import annotations

import argparse
from wsgiref.simple_server import make_server

from .main import app


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the Orga dashboard API.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface (default: %(default)s)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind (default: %(default)s)")
    return parser.parse_args()


def serve_app(host: str, port: int) -> None:
    with make_server(host, port, app) as server:
        print(f"Serving Orga Dashboard API on http://{host}:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Stopping server...")


def main() -> None:
    args = _parse_args()
    serve_app(args.host, args.port)


if __name__ == "__main__":
    main()
