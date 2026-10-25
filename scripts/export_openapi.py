"""Export FastAPI application OpenAPI schema to openapi.json.

Run via:
    python scripts/export_openapi.py
    or: make openapi
"""

import json
import sys
from pathlib import Path

# Add src to sys.path to enable execution without prior pip install
src_dir = Path(__file__).resolve().parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from urja_api.main import create_app


def export_openapi() -> None:
    app = create_app()
    openapi_schema = app.openapi()
    target_path = Path(__file__).resolve().parent.parent / "openapi.json"
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"Exported OpenAPI schema to {target_path}")


if __name__ == "__main__":
    export_openapi()
