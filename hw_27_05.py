

def divisors(number):
    div = 2
    proper_divisors = []
    while number != number or number != 1:
        if number % div == 0:
            number = number // div
            proper_divisors.append(div)
        else:
            div += 1
    return proper_divisors


def binary(number):
    bin_number = []
    while number > 0:
        if number % 2 == 0:
            bin_number.append(0)
        else:
            bin_number.append(1)
        number = number // 2
    return bin_number


def average():
    average_list = []
    stamp = 1
    while stamp <= 134:
        for x in range(stamp, stamp+10):
            x += 1
        average_list.append(x/10)
        stamp += 1
    return average_list


def fibo(x):
    if x == 0:
        return 1
    elif x == 1:
        return 1
    else:
        return fibo(x-1) + fibo(x-2)


def ziggurat(num):
    #have not done yet
    zig1 = [[num-num+1 for y in range(num)] for x in range(num)]
    zig2 = [[num-num+1 if y < num-3 or y > num-3 else num for y in range(num)] for x in range(num)]
    for x in range(num+3):
        print(zig1[x])
        print(zig2[x])
