# Errors and Exceptions

*"Errors should never pass silently. Unless explicitly silenced."*

## Catch narrowly

Catch the most specific exception that can actually be raised, around the smallest block that can
raise it. A wide `try` swallows bugs from code you never meant to guard.

**No**
```python
try:
    config = load(path)
    user = db.fetch(config.user_id)
    return render(user)
except Exception:
    return None
```

That hides a missing file, a database outage, a typo in `render`, and a `KeyError` from a bad
config key, and returns the same useless `None` for all of them.

**Yes**
```python
try:
    config = load(path)
except FileNotFoundError:
    raise ConfigMissingError(path) from None

user = db.fetch(config.user_id)
return render(user)
```

Bare `except:` is worse still - it catches `KeyboardInterrupt` and `SystemExit`, so it stops
Ctrl-C from working. If you truly need everything, `except Exception:` at least leaves those two
alone.

## Chain, do not discard

When you catch and re-raise, keep the cause.

**Yes**
```python
try:
    data = json.loads(text)
except json.JSONDecodeError as err:
    raise ConfigParseError(f"malformed config at {path}") from err
```

The traceback then shows both the wrapper and the original. Use `from None` only when the
original genuinely adds nothing and would confuse the reader - a `FileNotFoundError` under a
`ConfigMissingError` that already names the path, for instance.

Inside an `except` block, a bare `raise` re-raises the current exception with its traceback
intact. `raise err` loses part of it.

## Silence needs a reason

An exception you deliberately ignore gets a comment saying why, or a log line. Otherwise the
next reader cannot tell whether it was a decision or an oversight.

**Yes**
```python
try:
    cache.delete(key)
except CacheMissError:
    pass  # already gone; deleting is idempotent
```

**Yes**
```python
except UpstreamTimeout:
    logger.warning("metrics upload timed out, dropping batch of %d", len(batch))
```

**No**
```python
except Exception:
    pass
```

`contextlib.suppress` states the intent in one line:

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    path.unlink()
```

## Log the traceback

Inside an `except` block, `logger.exception` records the stack. `logger.error` does not.

```python
except StorageError:
    logger.exception("failed to persist session %s", session.id)
    raise
```

Do not both log and raise at every level - that produces the same error five times in the log.
Log where you handle it, raise where you do not.

## Designing your exceptions

One base class per package, so callers can catch everything you raise with a single clause.
Subclass from `Exception`, never `BaseException`.

```python
class StorageError(Exception):
    """Base for every error raised by this package."""


class SessionNotFoundError(StorageError):
    def __init__(self, session_id: str) -> None:
        super().__init__(f"no session {session_id}")
        self.session_id = session_id
```

Names end in `Error`. Carry the offending value as an attribute, not only inside the message
string - a caller that wants to retry needs the value, not a string to re-parse.

Reuse a builtin when it fits. `ValueError` for a bad value, `TypeError` for a wrong type,
`KeyError` for a missing key, `NotImplementedError` for an unfinished override. Inventing
`MyValueError` gains nothing.

## Raise, do not return a sentinel

**Yes**
```python
def fetch(session_id: str) -> Session:
    """Return the session.

    Raises:
        SessionNotFoundError: If no session has that id.
    """
```

**No**
```python
def fetch(session_id: str) -> Session | None:
    """Return the session, or None if it does not exist."""
```

A returned `None` gets ignored, and the failure surfaces later as an `AttributeError` far from
the cause. Return `None` only when absence is a normal, expected outcome the caller routinely
handles - a cache lookup, a `find_first`.

## Never `assert` for runtime validation

`python -O` strips every `assert` from the bytecode. Validation that disappears under a flag is
not validation.

**No**
```python
def withdraw(account, amount):
    assert amount > 0, "amount must be positive"
```

**Yes**
```python
def withdraw(account: Account, amount: Decimal) -> None:
    if amount <= 0:
        raise ValueError(f"amount must be positive, got {amount}")
```

`assert` is for tests, and for internal invariants that a bug would break rather than a user.

## Cleanup

Anything that must be released goes in a `with`. It runs on the exception path too, which is
what `try`/`finally` was for and why nobody should write that by hand any more.

```python
with open(path, encoding="utf-8") as f, lock:
    ...
```

Write your own with `contextlib.contextmanager`:

```python
from contextlib import contextmanager

@contextmanager
def transaction(conn):
    tx = conn.begin()
    try:
        yield tx
    except Exception:
        tx.rollback()
        raise
    else:
        tx.commit()
```

Never `return`, `break`, or `continue` inside a `finally` block - it discards an in-flight
exception and the failure vanishes.

## Validate at the boundary

Check input where it enters your system - the request handler, the CLI parser, the file reader -
and trust it inward. Validating the same value at every layer is noise; validating it nowhere is
the bug.

*"In the face of ambiguity, refuse the temptation to guess."* When input is malformed, raise.
Do not substitute a plausible default and carry on, because the caller then acts on data that was
never theirs.
