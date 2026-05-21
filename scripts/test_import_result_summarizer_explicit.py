import sys
sys.path.insert(0, r'e:/AI_Workspace/01_PROJECTS/AIDRA')
try:
    import backend.services.result_summarizer as rs
    print('Imported OK', hasattr(rs, 'summarize_results'))
    print('module file:', getattr(rs, '__file__', None))
    print('module dict keys:', list(rs.__dict__.keys()))
    try:
        import inspect
        print('\nSource:\n')
        print(inspect.getsource(rs))
    except Exception:
        print('Could not read source via inspect')
except Exception as e:
    import traceback
    traceback.print_exc()
