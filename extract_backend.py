import ast

with open('CBC_NLP_clean.py', 'r', encoding='utf-8') as f:
    source = f.read()

tree = ast.parse(source)

clean_body = []
for node in tree.body:
    if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef)):
        clean_body.append(node)
    elif isinstance(node, ast.Assign):
        # Only keep assignments to important global variables
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in ('nlp', 'knowledge_df', 'suggestion_df'):
                clean_body.append(node)
                break

clean_tree = ast.Module(body=clean_body, type_ignores=[])
clean_source = ast.unparse(clean_tree)

with open('backend.py', 'w', encoding='utf-8') as f:
    f.write(clean_source)
