import argparse
from pathlib import Path
from .loaders import load_directory

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="CSV → combined table")
    p.add_argument("--input", required=True, help="Folder with CSVs")
    p.add_argument("--limit", type=int, default=None, help="Row cap per file (dev aid)")
    return p.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)
    df = load_directory(Path(args.input), patterns=("*.csv",), limit=args.limit)

    outdir = Path("build")
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "combined.csv"
    df.to_csv(out, index=False)

    print(f"[file-fusion] rows={len(df)} cols={len(df.columns)}")
    print(f"[file-fusion] wrote {out}")

if __name__ == "__main__":
    main()
