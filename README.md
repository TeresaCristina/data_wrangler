Project anatomy
Code
src/data_wrangler/cli.py
What it is: The command-line entry point.

What it does:

Parses flags (at minimum: --input, optional --limit).

Calls load_directory(...) to ingest files from the folder you point at.

Writes the unified table to build/combined.csv.

Prints a quick summary (rows/cols).

Key pieces you’ll see:

parse_args(argv=None): defines the CLI flags.

main(argv=None): orchestrates discovery → load → save.