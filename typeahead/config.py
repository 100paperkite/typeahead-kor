from os.path import dirname, join

BASE_DIR = dirname(dirname(__file__))


class TestingConfig:
    DEBUG = True
    TESTING = True
    MAX_HEAP_SIZE = 2
    MAX_PREFIX_SIZE = 2
    INDEX_DIR = join(BASE_DIR, "tests/test_data")
    VERSION = "test"


class DevelopmentConfig:
    DEBUG = True
    MAX_HEAP_SIZE = 5
    MAX_PREFIX_SIZE = 5
    INDEX_DIR = join(BASE_DIR, "data/index")
    VERSION = "2.0"

