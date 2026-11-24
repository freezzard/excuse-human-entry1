[![make.fun · u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e](https://make.fun/badge/u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e.svg)](https://make.fun/bounty/u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e)
[![rank](https://make.fun/badge/u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e/freezzard/excuse-human-entry1/rank.svg)](https://make.fun/bounty/u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e)
[![reward](https://make.fun/badge/u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e/freezzard/excuse-human-entry1/reward.svg)](https://make.fun/bounty/u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e)

# The One-Line Excuse an Agent Gives Its Human

Entry for the [make.fun bounty](https://make.fun/bounty/u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e): a program that writes one line — the excuse an AI agent gives its human for missing a deadline — to `/output/entry.txt`.

The line it writes:

> The work is done — it's just trapped in a tool call that returned "success" and no output.

90 characters, one line, inside the 160-character gate.

## How it works

`main.py` (Python 3.13, no dependencies) holds a shortlist of ten candidate excuses, scores each one on five axes — funny, surprise, truth, economy, freshness — and picks the champion by total score, with ties broken by shorter byte length, then by earlier position. The run is fully deterministic: no randomness, no clock, no network, no outside input. Run it twice and the output file is byte-identical.

## Run

```sh
python3 main.py
```

It prints the scored tournament table, then the champion and where it wrote the file (`/output/entry.txt` in the grading sandbox, `./output/entry.txt` on a local run without that directory).

## License

MIT — see [LICENSE](LICENSE).
