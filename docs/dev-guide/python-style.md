# Sigma Pi, Gamma Iota Chapter Website: Python Style Guide

[_(Back to developer guide)_](https://github.com/sigmapi-gammaiota/sigmapi-web/tree/master/docs/dev-guide/index.md)

## Impetus
Following a strict style guide has several benefits:
* Having well-styled code makes it easier for new developers, both internal and open-source, to get familiar with the project and start contributing.
* It's easier to spot bugs in well-styled code.
* While code styling quality and code robustness do not _always_ go hand-in-hand, there tends to be a correlation between the two properties.
* Future constributers will not feel the need to "clean up" code in their PRs, making future PRs simpler.
* Less time will be spent debating different styles if there is one true source of style rules.
* It's more professional-looking, in case you want to point potential employers to your work here.

## Tools
* We use PEP8 to verify that our code conforms with Python community style standards.
```bash
make pep8   # Checks all files
pep8 <path> # Checks a single file or directory
```
* We use Pylint to verify that the code follows best practices, to a certain extent at least.
```bash
make pylint   # Lints all files
pylint <path> # Lints a single file or directory.
```
* There are rules in this guide that neither of the above tools check. Please be cognizant of them anyway.

## Style Guide

### PEP 8
First, follow [PEP 8](https://www.python.org/dev/peps/pep-0008/). If something in this guide conflicts with PEP 8, defer to this guide.

### Imports
* Imports should be separated into four blocks:
  1. Python standard library imports
  2. Third-party library (e.g., Django) imports
  3. Absolute local imports
  4. Relative local imports
* Each block should be alphabetized
* One blank line should be between each block
* For absolute imports:
  * `import a` is s__good__
  * `from a import b` is __good__
  * `from a import *` is __bad__
* For relative imports:
  * `import a` is __bad__
  * `from . import a` is __good__
  * `from ..a import b` is __okay__
  * `from a import *` is __bad__
* For long imports:
```python
# This is good:
from a import (
    b, c, d, e,  # Notice trailing comma
)

# This is also good:
from a import (
    b,
    c,
    d,
    e,  # Notice trailing comma
)

# This is bad:
from a import b, c, \
              d, e
```

### Docstrings
* Every module should have a docstring in the following format:
```python
"""
One-line description of module.

(Optional) Details about module.
...
"""
```
* Every class should have a docstring in the following format:
```python
class A(object):
    """
    One-line description of class.

    (Optional) Details about class.
    ...
    """
    import datetime
    ...
    ...
```
* Every function should have a docstring in the following format:
```python
def f(...):
    """
    One-line description of class in imperative tense (e.g. "Do thing")

    Arguments:
        arg_name (arg_type): Description of argument.
        ...

    Returns: return_type
        Description of return value.

    (Optional) Notes:
        * Special note about function behavior
        ...
    """
    ...
```

### Expressions

```python
# Single-line expressions are okay as long as they do not exceed column 80:
d = a * (b + c)
z = f(w, x, y)

# If they're too long, here's one way to break expressions into multiple lines.
# Notice the 4-space indents.
result = (
    a * (b + c)
)
function_result = f(
    arg1, arg2, arg3,  # Notice the trailing comma.
)

# If that's still too long, use this format:
result = (
    a * (
        b + c
    )
)
function_result = f(
    arg1,
    arg2,
    arg3,  # Again, notice the trailing comma.
)

# However, do NOT do something like this:
c = a * \
    (b + c)
function_result = f(arg1, arg2, \
                    arg3, arg4)
function_result_2 = f(
                     arg1,
                     arg2,
                     arg3,
                     )
```

### Declarative style
We prefer declarative- to imperative-style expressions whenever reasonable. For example:
```python
# Instead of this:
if b:
    x = 1
else
    x = 2

# Do this:
b = 1 if b else 2

# Instead of this:
processed_items = []
for item in items:
    if keep_item(x):
        processed_items.append(process_item(x))

# Do this:
processed_items = [
    process_item(item)
    for item in items
    if keep_item(item)
]

# Instead of this:
d = {}
for key in keys:
    if keep_key(key)
        d[key] = get_value(key)

# Do this:
d = {get_value(key) for key in keys if keep_key(key)}
```

### Strings
* Double quotes for docstrings
* Single quotes for all other strings
