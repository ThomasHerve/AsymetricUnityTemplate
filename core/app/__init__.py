import hug
from handlers import test, core


@hug.extend_api("")
def api():
    return [test, core]

