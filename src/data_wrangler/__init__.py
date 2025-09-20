from pathlib import Path
import pandas as pd # pyright: ignore[reportMissingModuleSource]

from .auxiliar import find_files, unify_columns, file_end
from .jsonndjson import load_json_any
from .logtxt import read_log_or_txt, parse_kv_line

__all__ = [
    "find_files", "load_json_any", "read_log_or_txt", "parse_kv_line",
    "unify_columns", "load_directory",
]

def load_directory(in_dir: Path,
                   patterns=file_end,
                   limit: int | None = None):
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
    return unify_columns(frames)