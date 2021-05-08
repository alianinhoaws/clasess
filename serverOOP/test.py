import boto3

def hello(name: str, nubmer: int):
    for x in range (nubmer):  #iterator only accepted like a cow
        print(name)


hello("ndannan",3)

n = 5
A = range(1,6)
print(*A)

print(type(A))  #generator arifmetic progression

A=[1,2,3,4,5]

print(type(A) == list)


a = [(1,10), (2,20), (3,30)]

for number, (angel, length) in enumerate(a):
    print(number, angel, length)\


s = {'moscow', 'spd'} #hesh fast operations IN, ADD as in dict!!!, unions

#the same dict

dict = {'Moscow': 24, 'SPB': 24}

for key,value in dict.items():
    print(key,value)

dict['Rostov'] = 22

print(dict)