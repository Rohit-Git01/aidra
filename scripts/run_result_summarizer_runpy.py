import runpy, sys
sys.path.insert(0, r'e:/AI_Workspace/01_PROJECTS/AIDRA')
try:
    d = runpy.run_path(r'e:/AI_Workspace/01_PROJECTS/AIDRA/backend/services/result_summarizer.py')
    print('keys:', [k for k in d.keys() if not k.startswith('__')])
    print('has summarize:', 'summarize_results' in d)
except Exception as e:
    import traceback
    traceback.print_exc()
