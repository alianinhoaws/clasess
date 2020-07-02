
url = '/user/adada'

method = 'DELETE'

def lalal(method):
    if url.startswith('/user/'):
        tag = 'User'
    methods = {
        "POST": 'self.post(tag)',
        "PUT": 'self.put(tag)',
        "DELETE": 'self.delete(tag, id)',
        "GET": 'self.get(tag, id)',
    }
    try:
        return methods[method]
    except Exception as exc:
        print(exc)

print(lalal(method))