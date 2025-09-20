from pathlib import Path
import sys
sys.path.insert(0, str(Path("src").resolve()))

from data_wrangler.auxiliar import find_files, load_json_any
import pandas as pd # pyright: ignore[reportMissingModuleSource]

patterns = ("*.csv","*.json","*.ndjson","*.jsonl")
root = Path("sample_data")

paths = find_files(root, patterns)
print("[discover]", [p.name for p in paths])

for p in paths:
    print(f"\n[file] {p.name}  (suffix={p.suffix.lower()})")
    try:
        if p.suffix.lower() == ".csv":
            df = pd.read_csv(p)
        else:
            df = load_json_any(p)
        print(" -> rows, cols =", df.shape)
        print(df.head(2))
    except Exception as e:
        print(" -> ERROR:", repr(e))
