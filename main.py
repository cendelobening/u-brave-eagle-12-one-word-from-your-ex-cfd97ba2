"""One Word From Your Ex.

Writes exactly one word -- the word an ex would use to describe the
entrant -- to entry.txt. Pure standard library.

Gate: /output/entry.txt must be UTF-8 text of 1 to 24 characters, not
only white space. This entry is one 10-letter word, no trailing newline.
"""

import os
import stat
import tempfile

WORD = "exhausting"
# Why this word: it is the word an ex actually says out loud -- not an
# insult, but a sigh. It is funny because the entrant plainly knows it,
# it stings because it is true, and everyone who has been in a draining
# relationship recognises it instantly. One plain word, no explanation
# needed, and no near-synonym ("tiring", "draining") lands quite as hard.


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    data = WORD.encode("utf-8")
    assert 1 <= len(data) <= 24, "word must be 1-24 characters"
    assert WORD.isalpha(), "must be a single alphabetic word"
    assert not any(ch.isspace() for ch in WORD), "must be a single word"

    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    os.chmod(target, 0o644)

    # Read back and verify: exact bytes, no trailing newline, mode 0644.
    with open(target, "rb") as fh:
        back = fh.read()
    assert back == data, "read-back mismatch"
    assert not back.endswith(b"\n"), "no trailing newline allowed"
    assert back.decode("utf-8").split() == [WORD], "must be exactly one word"
    mode = stat.S_IMODE(os.stat(target).st_mode)
    assert mode == 0o644, f"mode must be 0644, got {oct(mode)}"


if __name__ == "__main__":
    main()
