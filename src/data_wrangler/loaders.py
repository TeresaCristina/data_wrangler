from pathlib import Path
import pandas as pd



def find_files(in_dir: Path, patterns=(".csv",)):
    paths = []
    for pat in patterns:
        paths += sorted(Path(in_dir).rglob(pat))
    return [p for p in paths if p.is_file()]

def load_csv(path: Path, limit: int | None = None) -> pd.DataFrame:
    df = pd.read_csv(path, nrows=limit)
    df["source_file"] = str(path)
    return df

def unify_columns(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    cols = []
    for df in dfs:
        for c in df.columns:
            if c not in cols:
                cols.append(c)
    dfs2 = [df.reindex(columns=cols) for df in dfs]
    return pd.concat(dfs2, ignore_index=True)

def load_directory(in_dir: Path, patterns=("*.csv",), limit: int | None = None) -> pd.DataFrame:
    paths = find_files(in_dir, patterns)
    if not paths:
        raise FileNotFoundError(f"No files matched {patterns} under {in_dir}")
    frames = [load_csv(p, limit) for p in paths]
    return unify_columns(frames)
