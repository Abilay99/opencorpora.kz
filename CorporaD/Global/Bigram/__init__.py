__doc__ = """
    ...Bigrams
"""
import os
from .util import bigram
from .util import sozgebolu
try:
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    with open(version_file, 'r') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (running code interactively?)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
if __doc__ is not None:
    __doc__ += '\n    @version: ' + __version__