from pathlib import Path
import pandas as pd # pyright: ignore[reportMissingModuleSource]
from .logtxt import read_log_or_txt
from .jsonndjson import load_json_any

file_end = ["*.csv", "*.json", "*.ndjson", "*.jsonl", "*.log", "*.txt"]

# Finds and returns all the files that match the file_end list
def find_files(in_dir: Path, patterns=file_end):
    paths = []
    for pat in patterns:
        paths += sorted(Path(in_dir).rglob(pat))
    return [p for p in paths if p.is_file()]

def unify_columns(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    cols: list[str] = []
    for df in dfs:
        for c in df.columns:
            if c not in cols:
                cols.append(c)
    return pd.concat([df.reindex(columns=cols) for df in dfs], ignore_index=True)