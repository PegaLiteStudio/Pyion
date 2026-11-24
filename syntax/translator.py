"""
PyNova Language Translator
Converts PyNova source code (.pyn) with custom syntax features
into fully valid Python AST / code.

Custom constructs supported:
1. repeat <count>:      -> for _pynova_rep_L in _pynova_validate_repeat(<count>, L):
2. safe:                -> try: ... except Exception as _err: _pynova_handle_safe_error(...)
3. wait <duration>      -> _pynova_runtime_wait(<duration>, L)
4. <val> between <a> and <b> -> (((a) <= (val)) and ((val) <= (b)))
"""

import io
import re
import tokenize
from typing import List, Tuple, Optional


class PyNovaSyntaxError(SyntaxError):
    """Raised when PyNova source contains invalid custom syntax."""
    pass


def _find_left_operand(tokens: List[tokenize.TokenInfo], between_idx: int) -> Tuple[int, str]:
    """
    Finds the start index and text of the expression immediately preceding 'between'.
    Respects matched parentheses, brackets, and arithmetic operators.
    """
    paren_depth = 0
    idx = between_idx - 1
    stop_tokens = {tokenize.NEWLINE, tokenize.NL, tokenize.INDENT, tokenize.DEDENT}
    stop_names = {"if", "elif", "while", "and", "or", "not", "return", "in", "is", "assert"}
    
    while idx >= 0:
        t = tokens[idx]
        if t.type in stop_tokens:
            break
        if t.exact_type in {tokenize.RPAR, tokenize.RSQB, tokenize.RBRACE}:
            paren_depth += 1
        elif t.exact_type in {tokenize.LPAR, tokenize.LSQB, tokenize.LBRACE}:
            if paren_depth == 0:
                break
            paren_depth -= 1
        elif paren_depth == 0:
            if t.exact_type in {tokenize.COLON, tokenize.COMMA, tokenize.SEMI}:
                break
            if t.type == tokenize.NAME and t.string in stop_names:
                break
        idx -= 1
        
    start_idx = idx + 1
    if start_idx >= between_idx:
        raise PyNovaSyntaxError(f"Missing left operand for 'between' at line {tokens[between_idx].start[0]}")
    left_text = "".join(t.string + (" " if t.type != tokenize.OP else "") for t in tokens[start_idx:between_idx]).strip()
    return start_idx, left_text


def _find_right_operands(tokens: List[tokenize.TokenInfo], between_idx: int) -> Tuple[int, str, str]:
    """
    Finds '<low>' and '<high>' operands in: between <low> and <high>
    Returns (end_idx, low_text, high_text).
    """
    # 1. Scan for matching 'and' keyword at depth 0
    idx = between_idx + 1
    paren_depth = 0
    and_idx = -1
    
    while idx < len(tokens):
        t = tokens[idx]
        if t.type in {tokenize.NEWLINE, tokenize.NL}:
            break
        if t.exact_type in {tokenize.LPAR, tokenize.LSQB, tokenize.LBRACE}:
            paren_depth += 1
        elif t.exact_type in {tokenize.RPAR, tokenize.RSQB, tokenize.RBRACE}:
            if paren_depth == 0:
                break
            paren_depth -= 1
        elif paren_depth == 0 and t.type == tokenize.NAME and t.string == "and":
            and_idx = idx
            break
        idx += 1
        
    if and_idx == -1:
        line_num = tokens[between_idx].start[0]
        raise PyNovaSyntaxError(f"Malformed 'between' expression at line {line_num}: missing 'and' boundary.")
        
    low_text = "".join(t.string + (" " if t.type != tokenize.OP else "") for t in tokens[between_idx + 1:and_idx]).strip()
    if not low_text:
        raise PyNovaSyntaxError(f"Missing lower bound in 'between' at line {tokens[between_idx].start[0]}")
        
    # 2. Scan for high operand after 'and'
    idx = and_idx + 1
    paren_depth = 0
    stop_tokens = {tokenize.NEWLINE, tokenize.NL, tokenize.INDENT, tokenize.DEDENT}
    stop_names = {"and", "or", "if", "else"}
    
    while idx < len(tokens):
        t = tokens[idx]
        if t.type in stop_tokens:
            break
        if t.exact_type in {tokenize.LPAR, tokenize.LSQB, tokenize.LBRACE}:
            paren_depth += 1
        elif t.exact_type in {tokenize.RPAR, tokenize.RSQB, tokenize.RBRACE}:
            if paren_depth == 0:
                break
            paren_depth -= 1
        elif paren_depth == 0:
            if t.exact_type in {tokenize.COLON, tokenize.COMMA, tokenize.SEMI}:
                break
            if t.type == tokenize.NAME and t.string in stop_names:
                break
        idx += 1
        
    end_idx = idx
    high_text = "".join(t.string + (" " if t.type != tokenize.OP else "") for t in tokens[and_idx + 1:end_idx]).strip()
    if not high_text:
        raise PyNovaSyntaxError(f"Missing upper bound in 'between' at line {tokens[between_idx].start[0]}")
        
    return end_idx, low_text, high_text


def _translate_between_expressions(line_text: str) -> str:
    """
    Translates any '<val> between <low> and <high>' expressions in a single line or statement.
    """
    if "between" not in line_text:
        return line_text
        
    try:
        token_gen = tokenize.tokenize(io.BytesIO(line_text.encode("utf-8")).readline)
        tokens = list(token_gen)
    except tokenize.TokenError:
        return line_text
        
    # Find all 'between' keyword tokens
    between_indices = [i for i, t in enumerate(tokens) if t.type == tokenize.NAME and t.string == "between"]
    if not between_indices:
        return line_text
        
    # Process from right to left to keep earlier indices valid
    result = line_text
    for b_idx in reversed(between_indices):
        try:
            start_idx, val_expr = _find_left_operand(tokens, b_idx)
            end_idx, low_expr, high_expr = _find_right_operands(tokens, b_idx)
            
            # Start and end character offsets in line
            start_col = tokens[start_idx].start[1]
            end_col = tokens[end_idx - 1].end[1]
            
            replacement = f"(({low_expr}) <= ({val_expr}) <= ({high_expr}))"
            result = result[:start_col] + replacement + result[end_col:]
            
            # Re-tokenize for next iteration if multiple on same line
            tokens = list(tokenize.tokenize(io.BytesIO(result.encode("utf-8")).readline))
        except (PyNovaSyntaxError, IndexError):
            continue
            
    return result


def translate_pynova(source: str, filename: str = "<pynova>") -> str:
    """
    Translates PyNova source code (.pyn) into standard executable Python code.
    
    Preserves line-number correspondence wherever possible.
    """
    lines = source.splitlines(keepends=True)
    translated_lines: List[str] = []
    
    # Track safe blocks: stack of tuples (indentation_str, line_number)
    safe_stack: List[Tuple[str, int]] = []
    
    # Regex patterns for line-based custom syntax
    re_repeat = re.compile(r"^(\s*)repeat\s+(.+?):(.*)$")
    re_safe = re.compile(r"^(\s*)safe:\s*(?:#.*)?$")
    re_wait = re.compile(r"^(\s*)wait\s+(.+?)\s*(?:#.*)?$")
    
    def close_safe_blocks(current_indent: str) -> None:
        """Closes any safe blocks that have ended given the current indentation."""
        curr_len = len(current_indent)
        while safe_stack:
            top_indent, top_line = safe_stack[-1]
            if curr_len <= len(top_indent):
                # Safe block ended, emit except handler
                safe_stack.pop()
                handler = (
                    f"{top_indent}except Exception as _pynova_err_L{top_line}:\n"
                    f"{top_indent}    _pynova_handle_safe_error(_pynova_err_L{top_line}, {top_line})\n"
                )
                translated_lines.append(handler)
            else:
                break

    for line_idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        
        # Check if line has content (not comment, not blank) to calculate indentation
        if stripped and not stripped.startswith("#"):
            indent_match = re.match(r"^(\s*)", line)
            line_indent = indent_match.group(1) if indent_match else ""
            close_safe_blocks(line_indent)
            
        # 1. Match 'safe:'
        safe_match = re_safe.match(line.rstrip())
        if safe_match:
            indent = safe_match.group(1)
            safe_stack.append((indent, line_idx))
            translated_lines.append(f"{indent}try:\n")
            continue
            
        # 2. Match 'repeat <count>:'
        repeat_match = re_repeat.match(line.rstrip())
        if repeat_match:
            indent = repeat_match.group(1)
            count_expr = repeat_match.group(2).strip()
            rest = repeat_match.group(3)
            iter_var = f"_pynova_rep_L{line_idx}"
            if rest and rest.strip() and not rest.strip().startswith("#"):
                # Single-line suite: repeat 3: print("hi")
                suite = rest.strip()
                translated_lines.append(
                    f"{indent}for {iter_var} in _pynova_validate_repeat({count_expr}, {line_idx}):\n"
                    f"{indent}    {suite}\n"
                )
            else:
                translated_lines.append(
                    f"{indent}for {iter_var} in _pynova_validate_repeat({count_expr}, {line_idx}):\n"
                )
            continue
            
        # 3. Match 'wait <duration>'
        wait_match = re_wait.match(line.rstrip())
        if wait_match:
            indent = wait_match.group(1)
            duration_expr = wait_match.group(2).strip()
            translated_lines.append(
                f"{indent}_pynova_runtime_wait({duration_expr}, {line_idx})\n"
            )
            continue
            
        # 4. Check for 'between' in the line
        if "between" in line:
            translated_line = _translate_between_expressions(line)
            translated_lines.append(translated_line)
        else:
            translated_lines.append(line)
            
    # Close any unclosed safe blocks at EOF
    while safe_stack:
        top_indent, top_line = safe_stack.pop()
        handler = (
            f"{top_indent}except Exception as _pynova_err_L{top_line}:\n"
            f"{top_indent}    _pynova_handle_safe_error(_pynova_err_L{top_line}, {top_line})\n"
        )
        translated_lines.append(handler)
        
    # Inject runtime helpers header
    header = (
        "# --- PyNova Runtime Header ---\n"
        "from syntax.runtime import "
        "_pynova_validate_repeat, _pynova_runtime_wait, _pynova_handle_safe_error\n"
        "# -----------------------------\n"
    )
    
    return header + "".join(translated_lines)
