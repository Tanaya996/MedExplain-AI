import ast

with open('CBC_NLP.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

while True:
    code = ''.join(lines)
    try:
        ast.parse(code)
        break
    except SyntaxError as e:
        if e.lineno:
            print(f"Fixing syntax error at line {e.lineno}")
            lines[e.lineno - 1] = '# ' + lines[e.lineno - 1]
        else:
            print("Syntax error without lineno!")
            break

with open('CBC_NLP.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
