# Hello Universe


def have_palindrome_triangle(num: int):
    for i in range(1, num+1):
        print(int((10**i-1)/9)**2)

if __name__ == '__main__':
    have_palindrome_triangle(5)
