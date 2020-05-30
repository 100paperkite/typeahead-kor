from os.path import dirname, join

# SERVER
DEBUG = False
PORT = 5000

# INDEX
DEFAULT_VERSION = "2.0"

MAX_HEAP_SIZE = 5
MAX_PREFIX_SIZE = 5
INDEX_DIR = join(dirname(dirname(__file__)), "data/index")
