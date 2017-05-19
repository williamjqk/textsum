# if False:
#     from past.builtins import xrange
# import sys
# print(sys.version_info.major)

# import sys
# if sys.version_info.major == 3:
#     from past.builtins import xrange # NEED pip install future
#
# import sys
# if sys.version_info.major == 3:
#     import queue as Queue
#     from past.builtins import xrange # NEED pip install future

# compat.py only handel the compatibility of Python 2 & 3 for textsum
from compat import * # If Python 3, need "pip install future"

for i in xrange(10):
    print(i)
