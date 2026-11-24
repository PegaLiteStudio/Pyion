# Project Overview: PyNova (One-Page Academic Explanation)

**Student / Project Title:** PyNova — A Customized Python Distribution and Language Implementation  
**Base Implementation:** CPython (Official Python 3.12 / 3.10 Runtime)  
**Original Source Origin:** Python Software Foundation (`https://github.com/python/cpython` and `https://www.python.org/ftp/python/3.12.9/Python-3.12.9.tgz`)  
**Executable Location:** `D:\PyNova\dist\pynova.exe` (and `D:\PyNova\bin\pynova.exe`)

---

### 1. Motivation & Purpose
Standard Python requires repetitive boilerplate for routine real-world data handling (such as validating phone numbers, splitting names, parsing URLs) and basic control flows (such as fixed counting loops, error suppression blocks, inline pauses, and range bounds checks). PyNova was engineered to eliminate this boilerplate by integrating high-level "smart data types" into the standard library and introducing four intuitive, highly readable syntax constructs.

---

### 2. What Modifications Were Made
1. **CPython Source & Metadata Customization**:
   - `Include/patchlevel.h`: Embedded PyNova release identification macros (`PYNOVA_DISTRIBUTION_NAME`, `PYNOVA_DISTRIBUTION_VERSION`).
   - `Python/sysmodule.c`: Added the `flavour` attribute to `sys.implementation` returning `"PyNova"`.
   - `cpython/Lib/pynova/`: Integrated the smart data types directly into CPython's standard library directory.
2. **Language Syntax Engine (`syntax/`)**:
   - `translator.py`: A token-aware pre-execution translation engine that maps PyNova custom syntax directly into valid Python bytecode operations while preserving line numbers.
   - `runtime.py`: Validation handlers for loop ranges, wait limits, and safe error trapping.
   - `runner.py`: A native CLI runner and interactive REPL.
3. **Standalone Distribution Executable**:
   - Built a standalone Windows binary (`pynova.exe`, 13 MB) that embeds the full runtime and packages all dependencies without requiring any external tools or Visual Studio installations.

---

### 3. Smart Data Types (`from pynova import ...`)
- **`Person`**: Manages personal names; extracts `first_name`, `middle_name`, `last_name`, and formatted uppercase `initials`; accepts manual overrides for complex cultural names.
- **`PhoneNumber`**: Parses international phone numbers using official ITU-T numbering plans; extracts `country_code`, `national_number`, `country`, and checks syntactic validity (`is_valid`).
- **`EmailAddress`**: Validates syntax against RFC 5322; splits `username`, `domain`, and top-level `extension` (e.g., `ac.in`, `com`).
- **`URL`**: Parses web addresses into `protocol`, `domain`, `path`, and verifies HTTPS usage via `is_secure`.
- **`Address`**: Provides structured postal address storage (`city`, `state`, `country`, `postal_code`) and formats single-line and multi-line mailing labels.

---

### 4. Custom Language Syntax
- **`repeat <N>:`**: Concise loop repeating an indented block $N$ times. Replaces `for _ in range(N):` with type and non-negative value verification.
- **`safe:`**: Lightweight exception containment block. Catches non-fatal exceptions, logs diagnostic messages, and resumes program execution without crashing or silencing critical system interrupts.
- **`wait <sec>`**: Direct pausing statement supporting integer or float durations; enforces non-negative inputs.
- **`<val> between <A> and <B>`**: Natural, inclusive range condition evaluating whether $A \le val \le B$.

---

### 5. How It Works
When running `pynova.exe script.pyn`:
1. The script is processed by `syntax.translator`, which scans lexical tokens and block indentations.
2. Custom language constructs are translated into canonical AST/Python structures with runtime assertions.
3. The resulting translated code is compiled into bytecode and executed inside the embedded PyNova CPython runtime.
4. Any errors point directly back to the original `.pyn` source line numbers.

---

### 6. How to Run the Final Executable
- **Run the full test suite:**
  ```powershell
  python -m unittest discover -s D:\PyNova\tests -p "test_*.py"
  ```
- **Execute the complete demonstration program:**
  ```powershell
  D:\PyNova\bin\pynova.exe D:\PyNova\examples\complete_demo.pyn
  ```
- **Run an inline expression:**
  ```powershell
  D:\PyNova\bin\pynova.exe -c "repeat 2: print('PyNova running!')"
  ```
