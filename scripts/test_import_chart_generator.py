import sys
sys.path.insert(0, r'e:/AI_Workspace/01_PROJECTS/AIDRA')
import backend.services.chart_generator as cg
print('module file:', cg.__file__)
print('keys:', [k for k in cg.__dict__.keys() if not k.startswith('__')])
