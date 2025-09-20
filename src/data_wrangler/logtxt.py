from pathlib import Path
import re
import pandas as pd # pyright: ignore[reportMissingModuleSource]

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
        for _i, line in enumerate(f, 1):
            if limit is not None and len(rows) >= limit:
                break
            s = line.strip()
            if not s:
                continue
            rows.append(parse_kv_line(s))
    df = pd.DataFrame(rows)
    df["source_file"] = str(path)
    return df
