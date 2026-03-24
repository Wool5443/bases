"""Application entrypoint."""

from .ui import BaseConverterApp


def main() -> int:
    app = BaseConverterApp()
    return app.run(None)


if __name__ == "__main__":
    raise SystemExit(main())
