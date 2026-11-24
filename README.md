# PyNova: A Customized Python Distribution and Language Implementation

**PyNova** is a customized Python implementation and dialect based on the official CPython source tree. It enhances standard Python by introducing **five smart data types** for common domain modeling and **four new programming syntax constructs** designed to eliminate routine boilerplate while maintaining 100% compatibility with the broader Python ecosystem.

PyNova compiles into a self-contained Windows executable (`pynova.exe`) requiring zero installation of Visual Studio, C++ compilers, or external runtimes.

---

## Table of Contents

- [Architectural Overview](#architectural-overview)
- [Key Features](#key-features)
  - [1. Smart Data Types](#1-smart-data-types)
  - [2. New Programming Syntax](#2-new-programming-syntax)
- [File Format: `.py` vs `.pyn`](#file-format-py-vs-pyn)
- [Project Directory Structure](#project-directory-structure)
- [Getting Started & Usage](#getting-started--usage)
  - [Running Scripts](#running-scripts)
  - [Running Inline Code](#running-inline-code)
  - [Interactive REPL](#interactive-repl)
  - [Adding to System PATH](#adding-to-system-path)
- [Comprehensive Demonstration](#comprehensive-demonstration)
- [Automated Testing](#automated-testing)
- [Technical Architecture & Component Breakdown](#technical-architecture--component-breakdown)
- [Academic Summary](#academic-summary)

---

## Architectural Overview

PyNova combines three distinct software layers:

```
┌────────────────────────────────────────────────────────┐
│                   PyNova Programs                      │
│             (.pyn or standard .py files)               │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│             PyNova Syntax Engine (syntax/)             │
│  - Token-level analyzer & AST translator               │
│  - Syntactic desugaring for repeat, safe, wait, between│
│  - Strict boundary & type validation at runtime        │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│           Custom CPython Runtime & Distribution        │
│  - Customized Include/patchlevel.h & sysmodule.c       │
│  - Built-in Lib/pynova/ standard library package       │
│  - Packaged standalone Windows binary (pynova.exe)     │
└────────────────────────────────────────────────────────┘
```

1. **CPython Source Customizations**: Custom identification macros in `cpython/Include/patchlevel.h`, registration of the `"PyNova"` flavour in `sys.implementation`, and standard library integration.
2. **PyNova Standard Library (`Lib/pynova/`)**: Native Python classes providing structured handling of people, phone numbers, emails, URLs, and postal addresses.
3. **PyNova Syntax & Execution Engine (`syntax/`)**: A token-aware translation and execution pipeline that compiles custom language constructs into standard bytecode operations while preserving line numbers for debugging.

---

## Key Features

### 1. Smart Data Types

Imported directly via `from pynova import Person, PhoneNumber, EmailAddress, URL, Address`:

| Type | Purpose | Key Attributes & Properties | Example Usage |
|---|---|---|---|
| **`Person`** | Name parsing & manipulation | `first_name`, `middle_name`, `last_name`, `full_name`, `initials` | `p = Person("Sahil Hossain")`<br>`print(p.initials) # S.H.` |
| **`PhoneNumber`** | International phone validation | `country_code`, `national_number`, `country`, `formatted`, `is_valid` | `ph = PhoneNumber("+919876543210")`<br>`print(ph.country) # India` |
| **`EmailAddress`** | RFC 5322 email inspection | `address`, `username`, `domain`, `extension`, `is_valid` | `em = EmailAddress("user@example.com")`<br>`print(em.extension) # com` |
| **`URL`** | Web URL analysis & security | `protocol`, `domain`, `path`, `query`, `fragment`, `is_secure`, `is_valid` | `u = URL("https://example.com/docs")`<br>`print(u.is_secure) # True` |
| **`Address`** | Structured postal addresses | `city`, `state`, `country`, `postal_code`, `street`, `formatted`, `to_multiline()` | `a = Address(city="Agartala", ...)`<br>`print(a.formatted)` |

> **Note on Technical Precision**:
> - `PhoneNumber.is_valid` validates against ITU-T national numbering plans; it does not claim a line is actively subscribed.
> - `EmailAddress.is_valid` validates RFC syntax; it does not verify whether a physical mailbox exists.
> - `URL.is_secure` indicates HTTPS transport encryption; it does not verify website trust or content safety.

---

### 2. New Programming Syntax

PyNova introduces four high-level constructs designed to make code expressive and readable:

#### A. `repeat <count>:`
Repeats a block of code a specified number of times with non-negative integer validation.
```python
# Multi-line block
repeat 3:
    print("Welcome to PyNova!")

# Single-line suite
repeat 2: print("Quick repeat!")
```
*Equivalent standard Python:*
```python
for _ in range(3):
    print("Welcome to PyNova!")
```

#### B. `safe:`
Executes a block with automatic containment of non-fatal exceptions (derived from `Exception`). It logs a diagnostic warning and continues subsequent execution without crashing or silencing critical system signals (`KeyboardInterrupt`, `SystemExit`).
```python
safe:
    number = int("not-a-number")
    print(number)

print("Execution continues safely after the error.")
```

#### C. `wait <duration>`
Pauses execution for a specified duration in seconds. Accepts integers, floats, or expressions and enforces non-negative limits.
```python
print("Starting operation...")
wait 1.5
print("Operation resumed after 1.5s delay.")
```

#### D. `<value> between <lower> and <upper>`
A readable, inclusive range-comparison operator working seamlessly inside conditions and expressions.
```python
age = 25

if age between 18 and 60:
    print("Within permitted age range.")

# Works with complex expressions
score = 85
is_distinction = score between 80 and 100
```
*Equivalent standard Python:*
```python
if 18 <= age <= 60:
    print("Within permitted age range.")
```

---

## File Format: `.py` vs `.pyn`

`pynova.exe` natively accepts **both** file extensions:
- **`.pyn` (PyNova Script)**: Ideal for custom syntax programs. Differentiates PyNova dialect scripts and prevents false syntax error squiggles in standard code editors like VS Code or PyCharm.
- **`.py` (Standard Python Script)**: Supported unconditionally. You can rename any script to `.py` and execute it directly.

```powershell
.\bin\pynova.exe script.pyn
.\bin\pynova.exe script.py
```

---

## Project Directory Structure

```text
D:\PyNova\
├── bin\
│   └── pynova.exe                  # Standalone Windows executable
├── cpython\                        # CPython source distribution tree
│   ├── Include\patchlevel.h        # Customized distribution branding
│   ├── Python\sysmodule.c          # PyNova flavour registration in sys.implementation
│   └── Lib\pynova\                 # Integrated standard library module
├── dist\
│   └── pynova.exe                  # Packaged release binary
├── Lib\
│   └── pynova\                     # Smart data type package
│       ├── __init__.py
│       ├── person.py
│       ├── phone.py
│       ├── email.py
│       ├── url.py
│       └── address.py
├── syntax\                         # PyNova language engine
│   ├── translator.py               # Tokenizer and AST transformation pipeline
│   ├── runtime.py                  # Execution validators and runtime helpers
│   └── runner.py                   # CLI runner and interactive REPL
├── examples\                       # Example demonstration files
│   ├── complete_demo.pyn           # Full feature demonstration
│   ├── complete_demo.py            # .py format demonstration
│   ├── smart_types.pyn             # Smart data types demo
│   ├── repeat.pyn                  # Repeat loop demo
│   ├── safe.pyn                    # Safe block demo
│   ├── wait.pyn                    # Wait delay demo
│   └── between.pyn                 # Between operator demo
├── tests\                          # Automated unit test suite
│   ├── test_person.py
│   ├── test_phone.py
│   ├── test_email.py
│   ├── test_url.py
│   ├── test_address.py
│   └── test_syntax.py
├── README.md                       # Complete documentation
├── BUILD.md                        # Build and packaging instructions
└── HANDWRITTEN_EXPLANATION.md      # One-page academic summary for submission
```

---

## Getting Started & Usage

### Running Scripts

```powershell
Set-Location D:\PyNova

# Execute the master demonstration program
.\bin\pynova.exe examples\complete_demo.pyn

# Run individual feature examples
.\bin\pynova.exe examples\smart_types.pyn
.\bin\pynova.exe examples\repeat.pyn
.\bin\pynova.exe examples\safe.pyn
.\bin\pynova.exe examples\wait.pyn
.\bin\pynova.exe examples\between.pyn
```

### Running Inline Code (`-c`)

```powershell
# Test repeat syntax
.\bin\pynova.exe -c "repeat 3: print('Hello from PyNova!')"

# Test between comparison
.\bin\pynova.exe -c "x = 25; print('Eligible' if x between 18 and 60 else 'Ineligible')"

# Test smart types
.\bin\pynova.exe -c "from pynova import PhoneNumber; print(PhoneNumber('+919876543210').formatted)"
```

### Interactive REPL

Launch the interactive shell by running `pynova.exe` without arguments:

```powershell
.\bin\pynova.exe
```

```text
PyNova 1.0.0 [Custom CPython Distribution & Language]
Interactive Shell. Type 'exit()' or Ctrl-Z plus Return to exit.
>>> from pynova import Person
>>> p = Person("Ada Lovelace")
>>> p.initials
'A.L.'
>>> repeat 2:
...     print("PyNova Shell Active")
... 
PyNova Shell Active
PyNova Shell Active
>>> 45 between 40 and 50
True
>>> exit()
```

### Adding to System PATH (Optional)

To invoke `pynova` from any folder on your machine:

```powershell
$env:Path += ";D:\PyNova\bin"
pynova --version
pynova examples\complete_demo.pyn
```

---

## Comprehensive Demonstration

The master demonstration script ([`examples/complete_demo.pyn`](file:///D:/PyNova/examples/complete_demo.pyn)) exercises all 5 smart types and all 4 custom syntax features in a single program:

```python
from pynova import Person, PhoneNumber, EmailAddress, URL, Address

print("=== PyNova Demonstration ===")

# Smart data types
person = Person("Sahil Hossain")
phone = PhoneNumber("+919876543210")
email = EmailAddress("sahil@example.com")
website = URL("https://example.com/docs")
address = Address(
    city="Agartala",
    state="Tripura",
    country="India",
    postal_code="799001"
)

print("\nPerson:")
print(person.full_name)
print(person.initials)

print("\nPhone:")
print(phone.number)
print(phone.country_code)
print(phone.is_valid)

print("\nEmail:")
print(email.username)
print(email.domain)
print(email.is_valid)

print("\nWebsite:")
print(website.protocol)
print(website.domain)
print(website.is_secure)

print("\nAddress:")
print(address.formatted)

# repeat
print("\nRepeat demonstration:")
repeat 3:
    print("Welcome to PyNova!")

# safe
print("\nSafe demonstration:")
safe:
    number = int("not-a-number")
    print(number)

print("Program continues after the handled error.")

# wait
print("\nWait demonstration:")
print("Waiting...")
wait 2
print("Wait completed.")

# between
print("\nBetween demonstration:")
age = 25
if age between 18 and 60:
    print("Age is within the permitted range.")

print("\nPyNova demonstration completed.")
```

**Output:**
```text
[PyNova Safe Block Caught Error at line 51]: ValueError: invalid literal for int() with base 10: 'not-a-number'
=== PyNova Demonstration ===

Person:
Sahil Hossain
S.H.

Phone:
+919876543210
91
True

Email:
sahil
example.com
True

Website:
https
example.com
True

Address:
Agartala, Tripura - 799001, India

Repeat demonstration:
Welcome to PyNova!
Welcome to PyNova!
Welcome to PyNova!

Safe demonstration:
Program continues after the handled error.

Wait demonstration:
Waiting...
Wait completed.

Between demonstration:
Age is within the permitted range.

PyNova demonstration completed.
```

---

## Automated Testing

PyNova includes an automated unit test suite covering normal inputs, invalid inputs, edge cases, nested structures, and standard Python compatibility.

To run all 36 unit tests:

```powershell
Set-Location D:\PyNova
python -m unittest discover -s tests -p "test_*.py"
```

**Test Suite Coverage:**
- [`tests/test_person.py`](file:///D:/PyNova/tests/test_person.py): Two-word, three-word, single-word names, whitespace trimming, initials, explicit overrides, type errors.
- [`tests/test_phone.py`](file:///D:/PyNova/tests/test_phone.py): International numbers (India, US), national number extraction, invalid strings, non-string handling.
- [`tests/test_email.py`](file:///D:/PyNova/tests/test_email.py): Standard emails, domain normalization, multi-level TLDs (`.ac.in`), syntax validation.
- [`tests/test_url.py`](file:///D:/PyNova/tests/test_url.py): HTTP vs HTTPS, scheme extraction, query string and fragments, hostname normalization.
- [`tests/test_address.py`](file:///D:/PyNova/tests/test_address.py): Mandatory field validation, building/street support, single-line and multi-line formatting.
- [`tests/test_syntax.py`](file:///D:/PyNova/tests/test_syntax.py): Repeat iterations and negative/type rejections, safe non-fatal error handling and SystemExit preservation, wait delay measurement, between inclusive boundaries, and standard Python compatibility.

```text
Ran 36 tests in 0.117s
OK
```

---

## Technical Architecture & Component Breakdown

To maintain academic and technical integrity, PyNova clearly separates its components:

| Component | Nature of Implementation | Source Files |
|---|---|---|
| **CPython Core Identity** | C source and macro modifications in official CPython tree | `cpython/Include/patchlevel.h`<br>`cpython/Python/sysmodule.c` |
| **Smart Data Types** | Standard library extension module | `Lib/pynova/*.py`<br>`cpython/Lib/pynova/*.py` |
| **Language Syntax Translator** | Token-level lexical scanner and AST transformer | `syntax/translator.py` |
| **Runtime Validators** | Injected type and boundary enforcement functions | `syntax/runtime.py` |
| **CLI & Runtime Shell** | Entry point, script dispatcher, and interactive REPL | `syntax/runner.py` |
| **Distribution Executable** | Self-contained Windows PE binary | `bin/pynova.exe`<br>`dist/pynova.exe` |

---

## Academic Summary

For university project documentation and handwritten submissions, refer to [`HANDWRITTEN_EXPLANATION.md`](file:///D:/PyNova/HANDWRITTEN_EXPLANATION.md), which provides a structured one-page summary covering:
- Base implementation details and original source URLs.
- Justifications for added data types and syntax features.
- Operational mechanics of the translation and execution pipeline.
- Instructions for running the compiled executable.
