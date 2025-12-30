
---

# Shared Library Enumerator

A tool for inspecting and analyzing shared object (`.so`) files.

## Usage

### Running the Project

To run the project using the `uv` package manager, execute the following command:

```bash
uv run python
```

## Python API Examples

You can import and use the library in your Python scripts as shown below:

```python
import shared_lib_enumerator as sle

# Inspect a specific shared library
sle.inspect("/lib/libm.so.6")

# Inspect without sieving (filtering) symbols starting with "_"
sle.inspect("/lib/libm.so.6", sive_=False)
```

## Testing

To run the test suite and verify the output, execute:

```bash
uv run pytest ./tests/output_test.py
```

---
