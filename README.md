# bases-app

GTK4 Python application for converting non-negative integers from source bases 2..36 into target bases 2..10000.

For target bases above 36, the app still shows the digit-value list and reports that textual output is not supported.

## Run

```bash
PYTHONPATH=src python3 -m bases_app
```

## Test

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```
