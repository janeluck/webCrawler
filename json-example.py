import json
data_dict = {
    'head':{
        'title': 'awesome'
    },
    'body':{
        'content': 'awesome python'
    }
}

data_json = json.dumps(data_dict)
print(data_json)
print(type(data_json))
print(json.dumps(data_dict, indent=4))



print(json.loads(data_json))
print(type(json.loads(data_json)))