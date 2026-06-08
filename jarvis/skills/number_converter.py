"""Number converter — JARVIS converts between number bases."""

def to_binary(n: int) -> str:
    return f"{n} in binary is {bin(n)[2:]}, sir."

def to_hex(n: int) -> str:
    return f"{n} in hexadecimal is {hex(n)[2:].upper()}, sir."

def to_octal(n: int) -> str:
    return f"{n} in octal is {oct(n)[2:]}, sir."

def from_binary(b: str) -> str:
    try:
        n = int(b, 2)
        return f"Binary {b} = {n} in decimal, sir."
    except ValueError:
        return f"'{b}' is not valid binary, sir."

def from_hex(h: str) -> str:
    try:
        n = int(h.strip().lstrip("0x").lstrip("0X"), 16)
        return f"Hex {h.upper()} = {n} in decimal, sir."
    except ValueError:
        return f"'{h}' is not valid hexadecimal, sir."

def convert_base(value: str, from_base: int, to_base: int) -> str:
    try:
        decimal = int(value, from_base)
        if to_base == 2:   result = bin(decimal)[2:]
        elif to_base == 8: result = oct(decimal)[2:]
        elif to_base == 16: result = hex(decimal)[2:].upper()
        else: result = str(decimal)
        return f"{value} (base {from_base}) = {result} (base {to_base}), sir."
    except Exception as e:
        return f"Conversion failed: {e}"

def roman_numeral(n: int) -> str:
    vals = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),
            (50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]
    result = ""
    for v, s in vals:
        while n >= v:
            result += s; n -= v
    return f"Roman numeral: {result}, sir."

def parse_conversion(text: str) -> str:
    import re
    m = re.search(r"(\d+)\s+(?:to|in)\s+(binary|hex|octal|roman)", text, re.I)
    if m:
        n, target = int(m.group(1)), m.group(2).lower()
        if target == "binary": return to_binary(n)
        if target == "hex":    return to_hex(n)
        if target == "octal":  return to_octal(n)
        if target == "roman":  return roman_numeral(n)
    return "Try 'convert 42 to binary', sir."
