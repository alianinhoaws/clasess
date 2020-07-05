import re

STORAGE = {
    'companies': {12: {'arg': 'vr', 1:2}, 13: {'adad':'dadad'}},
    'users': {},
}


a = STORAGE.get('companies').get(12).update({'new_value': 'new_va'})

if not STORAGE.get('companies', {}).get(10):
    print('LALALLALALLALA')



result = re.findall('=(\w+)', 'id=2&name=companyX&address=London&tepephone=001')

print(result)