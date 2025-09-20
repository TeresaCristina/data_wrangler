# Project anatomy

## Code

```
src/data_wrangler/cli.py
```

The command-line entry point does the following:

- Parses flags (--input, [--limit]).

- Calls load_directory(...) to process the files.

- Writes the unified table into build/combined.csv.

- Prints a quick summary (rows/cols).

