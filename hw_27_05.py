

def divisors(number):
    div = 2
    proper_divisors = []
    while number != 1:
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


def average(window, lstart, lfinish) -> list:
    """Calculating moving average

    :param window: int number size of the window
    :param lstart: int number start of the list
    :param lfinish: int number finish of the list
    :return: list of average numbers
    """
    l = list(range(lstart, lfinish))
    average = []
    counter = 0
    for x in l:
        counter += 1
        x += 1
        if counter == window:
            average.append(x / window)
            counter = 0  #nulled counter to start cycle of a new window
    return average


def ziggurat(num):
    #have not done yet
    l = []
    n, y = num, num
    for x in range(1, num + num):
        if x <= n:
            l.append(x)
        else:
            y -= 1
            l.append(y)
    for x in range(1, num + num):
        print(l)


if __name__ == '__main__':
    print(average(5, 1, 100))
