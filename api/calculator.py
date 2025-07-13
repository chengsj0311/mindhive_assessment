import re

def calculate(text: str) -> str:
    # Match sequences like "7 * (3 + 2)" or "5 + 6 * 2"
    pattern = r"[0-9\.\s\+\-\*/\(\)]+"
    matches = re.findall(pattern, text)

    # Choose the longest valid-looking match
    if matches:
        expr = max(matches, key=len).strip()
        return f'{expr} = {eval(expr)}'
    else:
        return ""