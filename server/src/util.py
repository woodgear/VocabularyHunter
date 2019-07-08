def read_to_string(path):
    with open(path,'r',encoding='utf8') as f:
        output = f.read()
        return output