
# Coding conventions and documentation

## Coding conventions

The whole project will be developed using Python 3. Therefore, it has been decided to use PEP8 convention. The full documentation can be found on the official website www.pep8.org but here is a short cheat sheet:

```python
## IMPORT
# don't do: 
from time import *
(unless needed, then use the __all__ mechanism to prevent exporting globals)
# do:
from time import time
# or:
import time
# then prepends each method with module name: 
time.time()

## NAMING
Non-public methods and instance variables start with a leading underscore: _helper_method(), although not enforced by the compiler, the reader knows this is an internal method, not to be called from outside of the class.
If you need to use a Python keyword append an underscore: str_ = 'bob'
You probably want to avoid single-char variables all together, but if you use them never use these easily confused chars: 'l' (lowercase letter el), 'O' (uppercase letter oh), or 'I' (uppercase letter eye).
Use CapWords for class names.
Use short, all-lowercase names for modules.
Use lowercase and underscores for method names.
Constants are all uppercase, for example: PI, CONSUMER_KEY, CONSUMER_SECRET, etc.

## PROGRAMMING RECOMMENDATION
Lines should be < 80 characters long
my_var1 = "hello, "
my_var2 = "world!"
# don't do
my_var3 = my_var1 + my_var2
# do:
my_var3 = my_var1.join(my_var2)
```
It is highly recommended to use the pep8 python plugin: 
```bash
$ pip install pep8
$ pep8 digest.py 
digest.py:24:3: E111 indentation is not a multiple of four
digest.py:25:3: E111 indentation is not a multiple of four
digest.py:26:3: E111 indentation is not a multiple of four
digest.py:50:18: E225 missing whitespace around operator
digest.py:54:80: E501 line too long (83 > 79 characters)
```

## Documentation

The docstring used is Google Docstring type and the documentation will be generated using Sphinx. For exemple, functions should be described as follows: 
```python
def func(arg1, arg2):
    """Summary line.

    Extended description of function.

    Args:
        arg1 (int): Description of arg1
        arg2 (str): Description of arg2

    Returns:
        bool: Description of return value

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `arg2` is equal to `arg1`.

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> a=1
        >>> b=2
        >>> func(a,b)
        True

    """
    if arg1 == arg2:
        raise ValueError('arg1 must not be equal to arg2')

    return True
```

For a full description, see [this link.](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html#example-google)
