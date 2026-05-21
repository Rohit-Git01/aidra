import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    print('ROOT_DIR:', ROOT_DIR)
    import sys as _sys
    print('sys.path[0:5]:', _sys.path[0:5])
    import backend.services.result_summarizer as rs
    print('Imported OK', hasattr(rs, 'summarize_results'))
    print('dir:', [x for x in dir(rs) if 'summarize' in x.lower()])
except Exception as e:
    import traceback
    traceback.print_exc()
