import ast
p = r'e:/AI_Workspace/01_PROJECTS/AIDRA/backend/services/result_summarizer.py'
with open(p, 'r', encoding='utf-8') as f:
    src = f.read()
try:
    tree = ast.parse(src)
    func_names = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    print('functions in source:', func_names)
except Exception as e:
    import traceback
    traceback.print_exc()
