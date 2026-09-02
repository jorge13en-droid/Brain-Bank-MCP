"""Atalho de compatibilidade: `python server.py` continua funcionando.

O codigo real vive em `src/brain_bank/`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from brain_bank.server import main  # noqa: E402

if __name__ == "__main__":
    main()
