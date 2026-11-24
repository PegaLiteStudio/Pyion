# PyNova Build and Packaging Guide

This document describes how PyNova is built and packaged into a standalone Windows executable without requiring Microsoft Visual Studio.

---

## Prerequisites

- **Operating System**: Windows 10/11 64-bit
- **Python**: Python 3.10+ (with `pip`)
- **Required Packages**:
  ```powershell
  python -m pip install phonenumbers pyinstaller
  ```

---

## Build Steps

1. **Obtain Official CPython Source Tree**:
   The official CPython source tree was retrieved from python.org and placed in `cpython/`.

2. **Integrate PyNova Standard Library**:
   The `pynova` smart data types package resides in `Lib/pynova` and is integrated into `cpython/Lib/pynova`.

3. **Compile the Standalone Executable**:
   From `D:\PyNova`, execute:
   ```powershell
   python -m PyInstaller --onefile --noconfirm --name pynova --paths "Lib" --paths "." --hidden-import "phonenumbers" --hidden-import "pynova" --hidden-import "syntax.runtime" --hidden-import "syntax.translator" syntax\runner.py
   ```

4. **Verify Output**:
   The standalone executable is placed in `dist/pynova.exe` and copied to `bin/pynova.exe`.
