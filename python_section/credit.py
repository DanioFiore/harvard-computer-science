def get_long(user_input):
    while True:
        try:
            value = int(input(user_input))
            return value
        except ValueError:
            print("Invalid input, try again ")

def main():
    value = get_long("Number: ")
    tmp_value = value
    position = 1
    first_result = 0
    first_2_digits = 0
    number_of_digits = 0
    first_digit = 0

    # Process the number to calculate checksum and determine the first digits
    while tmp_value > 0:
        digit = tmp_value % 10
        if position % 2 == 0:
            multiplication = digit * 2
            if multiplication > 9:
                num_2 = multiplication % 10
                num_1 = (multiplication - num_2) // 10
                first_result += num_1 + num_2
            else:
                first_result += multiplication
        tmp_value //= 10
        if tmp_value < 100 and tmp_value > 10:
            first_2_digits = tmp_value
        elif tmp_value < 10 and tmp_value > 0:
            first_digit = tmp_value
        position += 1

    # Process the number to sum digits in odd positions
    position = 1
    while value > 0:
        digit = value % 10
        if position % 2 != 0:
            first_result += digit
        value //= 10
        number_of_digits += 1
        position += 1
    # Determine if the card is valid and its type
    if first_result % 10 != 0:
        print("INVALID")
    else:
        if (first_2_digits == 34 or first_2_digits == 37) and number_of_digits == 15:
            print("AMEX")
        elif 51 <= first_2_digits <= 55 and number_of_digits == 16:
            print("MASTERCARD")
        elif first_digit == 4 and (number_of_digits == 13 or number_of_digits == 16):
            print("VISA")
        else:
            print("INVALID")

main()
