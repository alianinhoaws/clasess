import re
telephone = '0675930219'
if re.fullmatch('[0-9]{10}', telephone):
    print('ok')


id = '122333'
a = re.fullmatch('[\d]*', id)
# print(a)

birthday = '33-12-1988'
a = re.fullmatch('\d{2}-\d{2}-\d{4}', birthday)
print(a)