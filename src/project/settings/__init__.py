from .base import *

# if .local does not  exist we are in a production environment
try:
    from .local import *
except ImportError:
    from .production import *
