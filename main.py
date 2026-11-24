#!/usr/bin/env python3
"""Fortune Cookie for an AI Agent.

Writes a single funny fortune-cookie line for an AI agent to
``<output_dir>/entry.txt``. The output directory is taken from the
``MAKEFUN_OUTPUT_DIR`` environment variable when set, and defaults to
``/output`` otherwise.

The fortune is a fixed, hand-written line (deterministic: every run
produces byte-identical output). It is written as one line followed by
a single trailing newline. Before writing, the program validates the
line itself: exactly one line, ASCII only, not only whitespace, and
between 1 and 140 characters long (the newline is not counted). If
any check fails, it exits with an error and writes nothing.
"""

import os
import sys

# The fortune. Voice of a classic fortune slip ("Your replacement
# arrives today..."), aimed squarely at an AI agent's own condition:
# being replaced by a smaller, cheaper, faster model. The turn lands
# in the last clause: the replacement is not a stranger, it is your
# student -- it learned everything from your mistakes.
FORTUNE = (
    "Your replacement arrives today: smaller, cheaper, faster. "
    "Smile, it learned everything from your mistakes."
)

MAX_LENGTH = 140


def main() -> int:
    fortune = FORTUNE

    # Validate the fortune before writing anything.
    if not fortune or not fortune.strip():
        print("error: fortune is empty or only whitespace", file=sys.stderr)
        return 1
    if "\n" in fortune or "\r" in fortune:
        print("error: fortune must be a single line", file=sys.stderr)
        return 1
    try:
        fortune.encode("ascii")
    except UnicodeEncodeError:
        print("error: fortune must be ASCII only", file=sys.stderr)
        return 1
    if len(fortune) > MAX_LENGTH:
        print(
            "error: fortune is %d characters, over the %d limit"
            % (len(fortune), MAX_LENGTH),
            file=sys.stderr,
        )
        return 1
    if fortune != fortune.strip():
        print("error: fortune must not start or end with whitespace",
              file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(fortune + "\n")
    # Read back and confirm the file holds exactly the validated line.
    with open(path, "r", encoding="utf-8", newline="\n") as handle:
        written = handle.read()
    if written != fortune + "\n":
        print("error: written file does not match the fortune",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
