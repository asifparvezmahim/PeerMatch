
# Just a cleanup script
import os
try:
    os.remove('test_output.py')
except:
    pass
try:
    os.remove('output.txt')
except:
    pass
