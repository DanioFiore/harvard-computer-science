def get_int(user_input):
    while True:
        try:
            value = int(input(user_input))
            return value
        except ValueError:
            print("Invalid input. Try again ")
def main():
    value = 0
    while value < 1 or value > 8:
        value = get_int("Height: ")

    for i in range(1, value + 1):
        new_value = i * 2

        print(' ' * (value - i), end='')
        for j in range(1, new_value + 1):
            print('#', end='')
            if j == new_value // 2:
                print('  ', end='')
        print()


main()
