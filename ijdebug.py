# import sys
# import os
# import runpy
#
# path = os.path.dirname(sys.modules[__name__].__file__)
# path = os.path.join(path, '..')
# sys.path.insert(0, path)
# runpy.run_module('replayenhancer', run_name='replayenhancer', alter_sys=True)

from replayenhancer import replayenhancer
if __name__ == '__main__':
    replayenhancer.main()