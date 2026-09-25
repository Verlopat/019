from __future__ import annotations

import logging
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

from proofaware.config import Config
from proofaware.runner import run


def main() -> None:
    load_dotenv()
    Path("outputs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    output = run(Config())
    print(f"Research run written to: {output}")


if __name__ == "__main__":
    main()
