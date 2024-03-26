import hug
from handlers import test


@hug.extend_api("")
def api():
    return [test]

