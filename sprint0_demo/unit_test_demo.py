def is_even(num):
    return num % 2 == 0

def fizzbuzz(num):
    str = ""
    if num % 3 == 0:
        str += "Fizz"
    if num % 5 == 0:
        str += "Buzz"
    return str

