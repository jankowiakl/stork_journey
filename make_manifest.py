#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

DEFAULT_EXTS = {".jpg", ".jpeg", ".png", ".webp"}  # allowed media extensions

def to_posix(rel_path: Path) -> str:
    return rel_path.as_posix()

def main():
    ap = argparse.ArgumentParser(description="Generate media_data/manifest.json for GitHub Pages.")
    ap.add_argument("--dir", default="media_data", help="Directory with media files (default: media_data)")
    ap.add_argument("--out", default=None, help="Output manifest path (default: <dir>/manifest.json)")
    ap.add_argument("--ext", action="append", default=None,
                    help="Allowed extension (repeatable), e.g. --ext .jpg --ext .jpeg")
    ap.add_argument("--recursive", action="store_true", default=True, help="Scan recursively (default: true)")
    args = ap.parse_args()

    base_dir = Path(args.dir)
    if not base_dir.exists() or not base_dir.is_dir():
        raise SystemExit(f"ERROR: Directory not found: {base_dir}")

    out_path = Path(args.out) if args.out else (base_dir / "manifest.json")

    exts = set(e.lower() for e in (args.ext if args.ext else list(DEFAULT_EXTS)))

    repo_root = Path.cwd().resolve()

    paths = []
    it = base_dir.rglob("*") if args.recursive else base_dir.glob("*")
    for p in it:
        if not p.is_file():
            continue
        if p.name.lower() == "manifest.json":
            continue
        if p.suffix.lower() not in exts:
            continue

        rel = p.resolve().relative_to(repo_root)
        paths.append(to_posix(rel))

    paths = sorted(set(paths))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(paths, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"OK: wrote {len(paths)} entries -> {out_path}")

if __name__ == "__main__":
    main()
