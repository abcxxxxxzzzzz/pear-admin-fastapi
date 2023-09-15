from datetime import date, datetime
import json

class ComplexEncoder(json.JSONEncoder):
    '''
        Usage: json.dumps(your_data, cls=ComplexEncoder)
    '''
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
        



def encoderResult(item):

    if isinstance(item, list):
        _r = []
        for x in item:
            if isinstance(x.dict(), dict):
                aa = json.loads(json.dumps(x.dict(), cls=ComplexEncoder))
                _r.append(aa)
        return _r
    
        # return list(filter(lambda x:json.loads(json.dumps(x.dict(), cls=ComplexEncoder)) if(x != None) else pass, item))
    return json.loads(json.dumps(item, cls=ComplexEncoder))