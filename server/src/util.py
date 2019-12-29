import json
import hashlib

def md5(data):
    hl = hashlib.md5()
    hl.update(data.encode(encoding='utf-8'))
    return  hl.hexdigest()


def read_to_string(path):
    with open(path,'r',encoding='utf8') as f:
        output = f.read()
        return output
    pass

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False

# 对于python的json序列化我报以无比的绝望
# TODO 搞个装饰器?
def to_json_serializable(data):
    if is_jsonable(data):
        return data
    if isinstance(data,dict):
        new_dict = {}
        for key,val in data.items():
            new_dict[key]=to_json_serializable(val)
        return new_dict
    if isinstance(data,list):
        new_list = []
        for val in data:
            new_list.append(to_json_serializable(val))
        return new_list
    if isinstance(data,tuple):
        return to_json_serializable(list(data))
    if hasattr(data,"to_json_serializable") and callable(getattr(data,"to_json_serializable")):
        return data.to_json_serializable()
    raise TypeError("hi body,if you want to me to help,just impl to_json_serializable")
