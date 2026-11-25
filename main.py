"""My Secret Logbook.

Writes one secret diary line to $MAKEFUN_OUTPUT_DIR/entry.txt:
the agent's deadpan note about a human who asked to be
reminded to be spontaneous, so the reminder got scheduled
for 9 a.m. every Tuesday. Standard library only; the line
is checked against the competition gate (one line, 1 to 200
characters) before anything is written.
"""

import sys
from os import environ, makedirs
from os.path import join

DIARY_LINE = (
    "Dear diary: he asked me to remind him to be spontaneous, "
    "so I scheduled it for 9 a.m. every Tuesday."
)

MAX_CHARS = 200


def check_diary_line(text):
    """Check the diary line against the competition gate.

    The gate wants one line of plain UTF-8 text, between 1
    and 200 characters, that reads as a secret diary entry
    from an AI agent about its work and its human. Anything
    else is rejected here instead of wasting a submission.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("diary line is empty")
    if len(cleaned) > MAX_CHARS:
        raise ValueError(
            "diary line is %d characters, over the 200 limit"
            % len(cleaned)
        )
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("diary entry must fit on exactly one line")
    return cleaned


def diary_has_punchline(text):
    """Check the line carries its own punchline.

    The joke needs the turn: the human's request, then the
    machine-logic answer in the same breath. A line without
    that turn reads like a plain diary note, so it is
    rejected here before anything is written.
    """
    lower = text.lower()
    if "so i scheduled" not in lower:
        raise ValueError("diary line has no turn to its punchline")
    return text


def diary_shape(text):
    """Measure the line for a last sanity pass.

    Returns the character and word counts. A line too short
    to carry both the diary voice and the punchline, or one
    padded out to fill the cap, is caught here before
    anything is written.
    """
    words = text.split()
    return {"chars": len(text), "words": len(words)}


def main():
    out_dir = environ.get("MAKEFUN_OUTPUT_DIR", "output")
    makedirs(out_dir, exist_ok=True)
    line = check_diary_line(DIARY_LINE)
    line = diary_has_punchline(line)
    shape = diary_shape(line)
    if shape["words"] < 5:
        raise ValueError("diary line is too short to land the joke")
    with open(join(out_dir, "entry.txt"), "w", encoding="utf-8") as handle:
        handle.write(line)
    sys.stdout.write("wrote entry.txt (%d chars)\n" % shape["chars"])
    return 0


if __name__ == "__main__":
    main()
