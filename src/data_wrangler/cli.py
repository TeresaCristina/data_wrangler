"""
data_wrangler.cli

Usage:
  python -m data_wrangler.cli --input <folder> [--limit N]
  eg.: 

- Discovers supported files in <folder>
- Merges them into a single table 
- Writes resuults into build/combined.csv
"""

import argparse
from pathlib import Path
from .loaders import load_directory

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Files → combined table")
    p.add_argument("--input", required=True, help="Folder with files")
    p.add_argument("--limit", type=int, help="Rows per file")
    return p.parse_args(argv)

def main(argv=None):
    args = parse_args(argv) # restrictions
    df = load_directory(Path(args.input), limit=args.limit)  # unified table
    # Check  directory
    outdir = Path("build")
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "combined.csv"
    df.to_csv(out, index=False)  # store unified table

    print(f"[data-wrangler] rows={len(df)} cols={len(df.columns)}")
    print(f"[data-wrangler] wrote {out}")

if __name__ == "__main__":
    main()
