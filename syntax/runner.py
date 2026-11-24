"""
PyNova CLI & Interpreter Launcher
Executes .pyn and .py scripts, evaluates inline code, or opens an interactive REPL.
"""

import sys
import os
import argparse
import traceback

# Ensure Lib and current directory are on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB_DIR = os.path.join(BASE_DIR, "Lib")
if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from syntax.translator import translate_pynova, PyNovaSyntaxError
from syntax.runtime import _pynova_validate_repeat, _pynova_runtime_wait, _pynova_handle_safe_error

VERSION = "1.0.0"
BANNER = (
    f"PyNova {VERSION} [Custom CPython Distribution & Language]\n"
    f"Interactive Shell. Type 'exit()' or Ctrl-Z plus Return to exit."
)


def run_code(source: str, filename: str = "<stdin>", global_scope: dict = None) -> None:
    """Translates and executes a PyNova code string."""
    try:
        translated = translate_pynova(source, filename)
        code_obj = compile(translated, filename, "exec")
        if global_scope is None:
            global_scope = {
                "__name__": "__main__",
                "__file__": filename,
                "__doc__": None,
                "__builtins__": __builtins__,
                "_pynova_validate_repeat": _pynova_validate_repeat,
                "_pynova_runtime_wait": _pynova_runtime_wait,
                "_pynova_handle_safe_error": _pynova_handle_safe_error,
            }
        exec(code_obj, global_scope)
    except PyNovaSyntaxError as se:
        sys.stderr.write(f"PyNovaSyntaxError: {se}\n")
        sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)


def run_file(filepath: str, script_args: list) -> None:
    """Executes a .pyn or .py script file with arguments."""
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        sys.stderr.write(f"PyNova Error: Cannot open file '{filepath}': No such file\n")
        sys.exit(1)
        
    script_dir = os.path.dirname(abs_path)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
        
    with open(abs_path, "r", encoding="utf-8") as f:
        source = f.read()
        
    sys.argv = [abs_path] + script_args
    run_code(source, filename=abs_path)


def repl() -> None:
    """Launches an interactive PyNova REPL."""
    print(BANNER)
    repl_globals = {
        "__name__": "__main__",
        "__doc__": None,
        "__builtins__": __builtins__,
        "_pynova_validate_repeat": _pynova_validate_repeat,
        "_pynova_runtime_wait": _pynova_runtime_wait,
        "_pynova_handle_safe_error": _pynova_handle_safe_error,
    }
    
    while True:
        try:
            line = input(">>> ")
            if not line.strip():
                continue
            if line.strip() in ("exit", "quit", "exit()", "quit()"):
                break
                
            # If block statement, collect continuation lines
            if line.rstrip().endswith(":"):
                block_lines = [line]
                while True:
                    continuation = input("... ")
                    if not continuation.strip() and not continuation.startswith(" "):
                        break
                    block_lines.append(continuation)
                full_source = "\n".join(block_lines) + "\n"
            else:
                full_source = line + "\n"
                
            translated = translate_pynova(full_source, filename="<stdin>")
            # Try evaluating as single expression first
            try:
                code_eval = compile(translated.strip(), "<stdin>", "eval")
                res = eval(code_eval, repl_globals)
                if res is not None:
                    print(repr(res))
            except SyntaxError:
                code_exec = compile(translated, "<stdin>", "exec")
                exec(code_exec, repl_globals)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting PyNova.")
            break
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]
        if first_arg in ("-v", "--version"):
            print(f"PyNova {VERSION} (based on CPython)")
            return
        elif first_arg in ("-h", "--help"):
            print("Usage: pynova [options] [script.pyn | script.py] [arguments]")
            print("\nOptions:")
            print("  -c <cmd>       Execute PyNova code passed in as string")
            print("  -v, --version  Print PyNova version and exit")
            print("  -h, --help     Show this help message and exit")
            return
        elif first_arg == "-c" and len(sys.argv) > 2:
            code = sys.argv[2]
            run_code(code, "<string>")
            return
        else:
            run_file(first_arg, sys.argv[2:])
            return
            
    repl()


if __name__ == "__main__":
    main()
