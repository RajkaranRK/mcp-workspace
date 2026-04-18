import json

from bson import json_util


def to_jsonable(value):
    return json.loads(json_util.dumps(value))
