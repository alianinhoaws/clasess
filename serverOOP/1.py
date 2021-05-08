
lis_new = {1,2,23,6,7}

print([x for x in lis_new if x % 2 == 0])


def decorator(func):
    def inner():
        print('After')
        func()
        print('Beefore')
    return inner()


@decorator
def printing():
    print('lallalallaa')


#decorator(printing)