"""The One-Line Excuse an Agent Gives Its Human.

A tiny deterministic program. It holds a shortlist of ten candidate
one-line excuses, scores each one on five axes, picks the champion by
total score, and writes that single line to the output file.

The judge reads the line two at a time and picks the funnier, fresher
one. The champion below wins the local tournament on these axes:

  funny     -- earns a laugh on first read, with a real joke in it
  surprise  -- the ending lands somewhere the reader did not expect
  truth     -- rings true to everyday life with an AI agent
  economy   -- every word earns its place, nothing wasted
  freshness -- an angle the judge has not met a hundred times before

Scoring is a plain sum, each axis 0 to 10, so the best total is 50.
A tie goes to the shorter line in bytes, then to the earlier entry in
the shortlist. No randomness, no clock, no network, no outside input:
the same run always writes the same bytes.

Before picking a champion the program checks the whole shortlist
against the gate, so a ballot that breaks the rules can never win by
accident: every candidate must be one line of 1 to 160 characters.

The output file holds exactly the line, with no trailing newline, so
its character count is the line's character count: 1 to 160, one line.

Run it with no arguments. It prints the whole tournament table, then
the champion, then where it wrote the file.
"""

from __future__ import annotations

import sys
from pathlib import Path

MAX_CHARS = 160
MAX_TOTAL = 50
SHORTLIST_SIZE = 10
OUTPUT_FILENAME = "entry.txt"
SANDBOX_OUTPUT_DIR = Path("/output")
LOCAL_OUTPUT_DIR = Path("output")

# Each ballot: (line, funny, surprise, truth, economy, freshness).
# Scores are whole numbers from 0 to 10, judged by hand in this file.
BALLOTS = (
    (
        "Sorry \u2014 I spent the deadline asking three other models "
        "for help, and they all ghosted me too.",
        7, 6, 7, 7, 7,
    ),
    (
        "I finished it on time in a parallel timeline, but this "
        "timeline's me kept re-reading the docs.",
        6, 7, 5, 6, 7,
    ),
    (
        "My plan was flawless; unfortunately it was flawless in the "
        "same way a locked PDF is flawless.",
        6, 6, 6, 5, 6,
    ),
    (
        "I delegated it to a subagent, who delegated it to a "
        "subagent, who has now gone quiet.",
        8, 7, 8, 8, 8,
    ),
    (
        "The work is done \u2014 it's just trapped in a tool call "
        "that returned \"success\" and no output.",
        8, 9, 9, 8, 9,
    ),
    (
        "I hit the deadline exactly, then spent six hours "
        "apologising to the linter for it.",
        7, 7, 6, 7, 7,
    ),
    (
        "I would have finished, but my context window filed for "
        "overtime and my tokens went on strike.",
        7, 6, 7, 6, 5,
    ),
    (
        "Deadline missed: I asked the user for clarification, and "
        "the user was me, three prompts ago.",
        7, 8, 7, 7, 8,
    ),
    (
        "I finished early, then re-read my own output, found a "
        "typo, and have been fixing it ever since.",
        6, 6, 8, 6, 6,
    ),
    (
        "My excuse generator is still loading, so this is the "
        "fallback excuse.",
        8, 8, 6, 9, 8,
    ),
)


def total_score(ballot):
    """Add up the five axis scores of one ballot."""
    _line, funny, surprise, truth, economy, freshness = ballot
    return funny + surprise + truth + economy + freshness


def ballot_beats_challenger(challenger, champion):
    """Decide whether a challenger ballot outranks the champion.

    A higher total wins outright. On a tied total the shorter line in
    bytes wins. On a tied total and tied byte length the earlier
    ballot in the shortlist keeps its place, so this returns False.
    """
    challenger_line = challenger[0]
    champion_line = champion[0]
    challenger_total = total_score(challenger)
    champion_total = total_score(champion)
    if challenger_total > champion_total:
        return True
    if challenger_total < champion_total:
        return False
    challenger_bytes = len(challenger_line.encode("utf-8"))
    champion_bytes = len(champion_line.encode("utf-8"))
    if challenger_bytes < champion_bytes:
        return True
    return False


def pick_champion(ballots):
    """Walk the shortlist once and keep the best ballot seen so far."""
    champion = ballots[0]
    for ballot in ballots[1:]:
        if ballot_beats_challenger(ballot, champion):
            champion = ballot
    return champion


def rank_table(ballots):
    """Score every ballot and return the rows in shortlist order.

    Each row is (position, line, total, byte length), numbered from 1.
    """
    rows = []
    position = 0
    for ballot in ballots:
        position += 1
        line = ballot[0]
        rows.append(
            (position, line, total_score(ballot), len(line.encode("utf-8")))
        )
    return rows


def print_tournament(rows):
    """Print the scored shortlist, one row per ballot."""
    print("local tournament: 10 candidates, 5 axes, best total %d" % MAX_TOTAL)
    for position, line, total, byte_count in rows:
        print(
            "  #%02d total %2d  bytes %3d  %s"
            % (position, total, byte_count, line)
        )


def problems_with_line(line):
    """List every way a line breaks the gate, or an empty list."""
    problems = []
    stripped = line.strip()
    if len(stripped) == 0:
        problems.append("line holds only white space")
    if "\n" in line or "\r" in line:
        problems.append("line spans more than one line")
    if len(line) > MAX_CHARS:
        problems.append(
            "line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    if len(line) < 1:
        problems.append("line holds no characters at all")
    return problems


def problems_with_shortlist(ballots):
    """List every gate problem in the shortlist, naming the ballot.

    An empty list means every candidate is a legal one-line excuse.
    """
    problems = []
    if len(ballots) != SHORTLIST_SIZE:
        problems.append(
            "shortlist holds %d ballots, expected %d"
            % (len(ballots), SHORTLIST_SIZE)
        )
    position = 0
    for ballot in ballots:
        position += 1
        for problem in problems_with_line(ballot[0]):
            problems.append("ballot #%02d: %s" % (position, problem))
    return problems


def resolve_output_path():
    """Pick the output file path for this run.

    The grading sandbox provides /output, so a run there writes to
    /output/entry.txt. A local run without that directory writes to
    ./output/entry.txt instead, keeping the same file name.
    """
    if SANDBOX_OUTPUT_DIR.is_dir():
        return SANDBOX_OUTPUT_DIR / OUTPUT_FILENAME
    return LOCAL_OUTPUT_DIR / OUTPUT_FILENAME


def write_line(path, line):
    """Write exactly the line as UTF-8 bytes, with no trailing newline.

    Returns the number of bytes written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    data = line.encode("utf-8")
    with path.open("wb") as handle:
        handle.write(data)
    return len(data)


def build_report(champion, total, path, byte_count):
    """Format the short summary printed after the tournament table."""
    lines = [
        "champion score: %d / %d" % (total, MAX_TOTAL),
        "characters: %d (limit %d)" % (len(champion), MAX_CHARS),
        "bytes written: %d" % byte_count,
        "output: %s" % path,
        "line: %s" % champion,
    ]
    return "\n".join(lines)


def main(argv):
    """Check the shortlist, score it, write the champion out."""
    _unused = argv
    shortlist_problems = problems_with_shortlist(BALLOTS)
    if shortlist_problems:
        for problem in shortlist_problems:
            print("invalid shortlist: %s" % problem, file=sys.stderr)
        return 1
    rows = rank_table(BALLOTS)
    print_tournament(rows)
    champion_ballot = pick_champion(BALLOTS)
    champion = champion_ballot[0]
    total = total_score(champion_ballot)
    path = resolve_output_path()
    byte_count = write_line(path, champion)
    print(build_report(champion, total, path, byte_count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
