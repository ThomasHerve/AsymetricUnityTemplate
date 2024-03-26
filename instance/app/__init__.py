import hug
from handlers import test, app


@hug.extend_api("")
def api():
    return [test, app]

