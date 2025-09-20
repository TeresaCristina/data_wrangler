from pathlib import Path
import json
import pandas as pd # pyright: ignore[reportMissingModuleSource]

def load_json_any(path: Path, limit: int | None = None) -> pd.DataFrame:
    text = Path(path).read_text(encoding="utf-8-sig", errors="ignore")

    # Try NDJSON line-by-line first
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

    # Fallback: array/object JSON
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
