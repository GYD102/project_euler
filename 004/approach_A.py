from math import ceil

def has_3d_factor(n):
    i = ceil(n ** 0.5)
    if i - 99 < 1000 - i:
        while i > 99:
            if n % i == 0:
                return True
            i -= 1
    else:
        while i < 1000:
            if n % i == 0:
                return True
            i += 1
    return False


# takes a number and makes an even-lengthed palindrome:
# 123 becomes 123321
def even_pali(n):
    s = str(n)
    n = n * (10 ** len(s))
    n += int(s[::-1])
    return n

if __name__ == "__main__":
    i = 999
    while True:
        if has_3d_factor(even_pali(i)):
            print(i)
            break
        i -= 1


