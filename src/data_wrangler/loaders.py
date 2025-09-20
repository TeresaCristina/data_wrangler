from pathlib import Path
import re, json
import pandas as pd # pyright: ignore[reportMissingModuleSource]

def find_files(in_dir: Path, patterns=("*.csv", "*.json", "*.ndjson", "*.jsonl", "*.log", "*.txt")):
    paths = []
    for pat in patterns:
        paths += sorted(Path(in_dir).rglob(pat))
    return [p for p in paths if p.is_file()]

def load_json_any(path: Path, limit: int | None = None) -> pd.DataFrame:
    # content-aware: tries NDJSON first, then JSON array/object
    text = Path(path).read_text(encoding="utf-8-sig", errors="ignore")

    rows, ndjson_ok = [], True
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        try:
            rows.append(json.loads(s))
        except json.JSONDecodeError:
            ndjson_ok = False
            break
    if ndjson_ok and rows:
        if limit is not None:
            rows = rows[:limit]
        df = pd.DataFrame(rows)
        df["source_file"] = str(path)
        return df

    data = json.loads(text)
    if isinstance(data, list):
        if limit is not None:
            data = data[:limit]
        df = pd.DataFrame(data)
    else:
        df = pd.json_normalize(data)
        if limit is not None:
            df = df.head(limit)
    df["source_file"] = str(path)
    return df

def load_directory(in_dir: Path, patterns=("*.csv", "*.json", "*.ndjson", "*.jsonl", "*.log", "*.txt"), limit: int | None = None) -> pd.DataFrame:
    paths = find_files(in_dir, patterns)
    if not paths:
        raise FileNotFoundError(f"No files matched {patterns} under {in_dir}")
    frames = []
    for p in paths:
        suf = p.suffix.lower()
        if suf == ".csv":
            frames.append(pd.read_csv(p, nrows=limit).assign(source_file=str(p)))
        elif suf in {".json", ".ndjson", ".jsonl"}:
            frames.append(load_json_any(p, limit))
        elif suf in {".log", ".txt"}:
            frames.append(read_log_or_txt(p, limit))
        else:
            continue
    # union-of-columns (keep yours if you already have it)
    cols = []
    for df in frames:
        for c in df.columns:
            if c not in cols:
                cols.append(c)
    return pd.concat([df.reindex(columns=cols) for df in frames], ignore_index=True)

_KV_RE = re.compile(r'(\S+?)=("[^"]*"|\S+)')

def parse_kv_line(line: str) -> dict:
    pairs = _KV_RE.findall(line)
    if not pairs:
        return {"raw": line.strip()}
    out = {}
    for k, v in pairs:
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        out[k] = v
    return out

def read_log_or_txt(path: Path, limit: int | None = None) -> pd.DataFrame:
    rows = []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            if limit is not None and len(rows) >= limit:
                break
            s = line.strip()
            if not s:
                continue
            rows.append(parse_kv_line(s))
    df = pd.DataFrame(rows)
    df["source_file"] = str(path)
    return df

