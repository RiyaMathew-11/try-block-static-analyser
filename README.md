# Static Analyser - Identifying print/log statements in try blocks

This tool **finds print statements or logs** in Python code that are **created within `try` blocks**. It grew out of a personal habit of keeping print/log statements in try blocks for debugging, that were often forgotten and left in the code before pushing to production 😅. (often happens with [JavaScript](https://github.com/fossunited/fossunited/pull/589#discussion_r1742236197) too)

## Why?

`print()` statements are often added in try blocks for debugging, like in the case of printing the result of computations or status flags. However, these statements are typically not suitable for production environments. Proper logging should be done in `except` blocks once the exception is caught, or in the `finally` block.

## Includes: 

- Analysing of single Python script files for print/log statements within try blocks
- Modular design for proper extensions and maintenance: 
    - The `StaticAnalyser` class forms the base that carries input and output mechanisms
    - The `PatternIdentifier` forms an abstraction layer. Any new pattern checks can be plugged in here.
- Outputs findings to console or a chosen report file.



## How to Run:

First, clone this repo and add your needed input file to analyse.

**1. To analyse a file:**

```python main.py [input_file]```

For example:

```python main.py sample_test_file.py```

**2. To save the output to a file:**

```python main.py [input_file] -s [report_file]```

or

```python main.py [input_file] > [report_file]```

Note: You can use either `-s` or `--save` to specify the report file.

**3. To run tests:**

`python -m unittest test_static_analyser.py`



## Dependencies
There are no external dependencies. It relies heavily on Python's built-in `ast` module for parsing and analysing Python code.

## Future Extensions

- Scan a bigger codebase rather than a single file at a time.
- Detect unwanted `console.log()` statements in JavaScript files.
    - There is a [plugin](https://www.npmjs.com/package/babel-plugin-transform-remove-console) that removes all console calls. However seems, this needs to be directly added into project's workflow, and not be used as a tool.
- Rewrite as a pylint or flake8 plugin with custom rules rather than using `ast` (Hypothesis: improves integration and maintenance)
- Research and implement additional pattern checks to improve code quality.
    - Considered to make a check for writing tests - checks if tests are done on air-tight environments. 
    - Often this best practice is violated, leading to the database getting exhausted or corrupted.