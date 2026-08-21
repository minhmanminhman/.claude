# Testing with pytest

This file covers the Python-specific mechanics. For what to test, how much, and the
red-green-refactor loop, use the `testing-strategy` and `tdd` skills.

## Plain functions, plain assert

No class, no `self`, no `assertEqual`. pytest rewrites the `assert` so a failure shows both sides.

```python
def test_parse_strips_whitespace():
    assert parse("  a, b  ") == ["a", "b"]
```

Failure output:

```
E       assert ['a', 'b '] == ['a', 'b']
E         At index 1 diff: 'b ' != 'b'
```

`unittest.TestCase` still works, and in a codebase already using it, keep using it. In new code
the class adds ceremony and gives nothing back.

## Naming

Long and descriptive. A good name is the docstring.

**Yes**
```python
def test_fetch_raises_when_session_expired(): ...
def test_retry_stops_after_max_attempts(): ...
def test_parse_returns_empty_list_for_blank_input(): ...
```

**No**
```python
def test_fetch(): ...
def test_fetch_2(): ...
def test_edge_case(): ...
```

Pattern that carries: `test_<unit>_<expected>_when_<condition>`. When a test fails in CI, the
name alone should tell you what broke.

## parametrize instead of copy-paste

```python
import pytest

@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("1kb", 1024),
        ("1MB", 1_048_576),
        ("0", 0),
        pytest.param("", 0, id="empty-string"),
        pytest.param("-1kb", None, marks=pytest.mark.xfail(reason="negatives unsupported")),
    ],
)
def test_parse_size(raw, expected):
    assert parse_size(raw) == expected
```

Each case reports as its own test, so one failing case does not hide the rest. Use `id=` when the
generated name would be unreadable.

## Exceptions

```python
def test_withdraw_rejects_negative_amount():
    with pytest.raises(ValueError, match="must be positive"):
        withdraw(account, Decimal("-5"))
```

`match` is a regex against the message. Without it, the test passes on any `ValueError`,
including one raised by a typo three lines earlier.

To inspect the exception:

```python
with pytest.raises(SessionNotFoundError) as excinfo:
    fetch("missing")
assert excinfo.value.session_id == "missing"
```

## Built-in fixtures worth knowing

```python
def test_writes_report(tmp_path):
    out = tmp_path / "report.txt"       # real Path, torn down automatically
    write_report(out, rows)
    assert out.read_text(encoding="utf-8").startswith("Total")


def test_uses_env_token(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "abc")      # restored after the test
    monkeypatch.setattr(client, "sleep", lambda _: None)
    assert build_headers()["Authorization"] == "Bearer abc"


def test_warns_on_deprecated_flag(caplog):
    with caplog.at_level(logging.WARNING):
        run(legacy=True)
    assert "deprecated" in caplog.text


def test_prints_summary(capsys):
    main()
    assert "3 files" in capsys.readouterr().out
```

`tmp_path` and `monkeypatch` replace nearly all hand-written setup and teardown, and they clean
up even when the test fails.

## Your own fixtures

```python
@pytest.fixture
def store():
    s = SessionStore(":memory:")
    yield s
    s.close()


@pytest.fixture
def session(store):          # fixtures compose
    return store.create(user_id="u1")
```

Put shared fixtures in `conftest.py` at the level where they apply. Scope wider only when setup
is genuinely expensive - `scope="module"` or `"session"` means state leaks between tests, which
is how order-dependent failures start.

Build objects with a factory function when the test needs to vary one field:

```python
def make_order(**overrides) -> Order:
    return Order(**{"id": "o1", "total": Decimal("10"), "items": [], **overrides})


def test_rejects_empty_order():
    with pytest.raises(EmptyOrderError):
        charge(make_order(items=[]))
```

Each test states only what it cares about, and adding a required field to `Order` is a one-line
fix rather than a hundred.

## Isolation

No real network, no real database, no dependence on the clock or on the current directory.

```python
def test_expiry_uses_injected_clock():
    session = Session(created_at=datetime(2024, 1, 1, tzinfo=UTC), ttl=timedelta(hours=1))
    assert session.is_expired(now=datetime(2024, 1, 1, 2, tzinfo=UTC))
```

Passing `now` in beats patching `datetime`. Design for the seam rather than reaching for a mock.

When you must patch, patch where the name is *used*, not where it is defined:

```python
monkeypatch.setattr("myapp.sessions.requests.get", fake_get)   # not "requests.get"
```

## Never let an unfinished test pass

```python
def test_handles_partial_upload():
    assert False, "TODO(#88): finish once the resume endpoint lands"
```

A silently passing empty test is worse than no test, because the coverage number says you are
covered.

## Running

```bash
pytest                       # everything
pytest -x                    # stop at the first failure
pytest -k "expired"          # tests whose name matches
pytest --lf                  # only what failed last run
pytest -q                    # quiet
```
