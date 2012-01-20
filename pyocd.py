import re
import os

PATH = "<path_goes_here>"

def to_uppr_enum(match):
    """convert second group to upper case, used to convert myEnum_e to eMyEnum"""
    return match.group(1) + 'e' + match.group(2).upper() + match.group(3) + match.group(4)

for path, dir, files in os.walk(PATH):
    for file in files:
        filepath = os.path.join(path, file)
        ext = os.path.splitext(filepath)[1]
        if ext == '.cpp' or ext == '.h':
            with open(filepath, 'r') as f:
                data = re.sub(r'\( ', '(', f.read())
                data = re.sub(r' \)', ')', data)
                data = re.sub(r'\[ ', '[', data)
                data = re.sub(r' \]', ']', data)
                data = re.sub(r'\<[ \t]*(\S+)[ \t]*\>', r'<\1>', data)
                data = re.sub(r'(\/*[ \t]*)(.*[a-zA-Z0-9_]+.*)\{[ \t]*\n', r'\1\2\n\1{\n', data)
                data = re.sub(r'if\(', r'if (', data)
                data = re.sub(r'for\(', r'for (', data)
                data = re.sub(r'while\(', r'while (', data)
                data = re.sub(r'switch\(', r'switch (', data)
                data = re.sub(r'(\/*[ \t]*)\}[ \t]*else', r'\1}\n\1else', data)
                data = re.sub(r'#if !defined\((.+)\)', r'#ifndef \1', data)
                data = re.sub(r'([^a-z0-9])([a-zA-Z])([a-zA-Z0-9]*)_e([^a-zA-Z0-9])', to_uppr_enum, data)
            with open(filepath, 'w') as f:
                f.write(data)
