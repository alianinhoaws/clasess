
def insert_sort(array):
    #  Iterate through len of given array
    for x in range(1, len(array)):
        while x > 0 and array[x - 1] > array[x]:    #always swap if > previous
            array[x], array[x - 1] = array[x - 1], array[x]
            x -= 1  # decrease X to go from right to left changing positions of element to sort them min goes to right by swap
    return array


def choice_sort(array):
    for start in range(0, len(array) - 1):  # iterate thought all array
        for find_min in range(start + 1, len(
                array)):  # try to find MIN in array iterating from start+1 and swap array[0] with array[min]
            if array[find_min] < array[start]:
                array[start], array[find_min] = array[find_min], array[start]
    return array


def bubble_sort(array):
    for x in range(1, len(array) - 1):
        for y in range(0, len(array) - 1):
            # go thought all array and swap bigger with smaller each iteration to the right
            if array[y] > array[y + 1]:
                array[y], array[y + 1] = array[y+1], array[y]
    return array


def merge(A, B):
    # A = [1,3,5,7] (index I)
    # B = [2,4,6,10] (index K)
    # C = [0,0,0,0,0,0,0] (len A+B)
    # will be if A[0] < B[0] add to C[0]
    # check if len A and len B else: add all elements from last one
    C = [0] * (len(A)+len(B))
    i = k = n = 0
    while i < len(A) and k < len(B):  # arrays are in borders
        if A[i] <= B[k]:
            C[n] = A[i]
            i += 1
            n += 1
        else:
            C[n] = B[k]
            k += 1
            n += 1
    while i < len(A):
        C[n] = A[i]
        i += 1
        n += 1
    while k < len(B):
        C[n] = B[k]
        k += 1
        n += 1
    return C


def merge_sort(array):
    if len(array) <= 1:
        return array
    middle = len(array)//2
    A = [array[i] for i in range(0, middle)]
    B = [array[i] for i in range(middle, len(array))]
    merge_sort(A)
    merge_sort(B)
    C = (merge(A, B))
    for i in range(len(array)):
        array[i] = C[i]
    return C


if __name__=='__main__':
    print(merge_sort([1,5,7,2,6,8,9,2]))
    print(bubble_sort([1,5,7,2,6,8,9,2]))
    print(choice_sort([1,5,7,2,6,8,9,2]))
    print(insert_sort([1,5,7,2,6,8,9,2]))
