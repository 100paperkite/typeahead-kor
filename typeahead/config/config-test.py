from os.path import join,dirname

BASE_DIR = dirname(dirname(dirname(__file__)))

DEBUG = True
TESTING = True

INDEX_DIR = join(BASE_DIR, "tests/data/index")