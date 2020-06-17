# rearrangement factorial


def swap_generation(word):
    if len(word) == 0:
        yield ""
    else:
        for m in range(len(word)):  # for each letter
            for n in swap_generation(word[0:m] + word[m+1:]):
                yield word[m]+n


if __name__=="__main__":
    for x in swap_generation('swap'):
        print(x)