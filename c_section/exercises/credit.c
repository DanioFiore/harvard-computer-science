/**
 * Launch in the terminal "make credit" to create the binary code and next launch "./credit" to execute the program.
 * You have to enter a credit card number and the program will say if is a VISA, AMEX, MASTERCARD or INVALID
*/
#include <cs50.h>
#include <stdio.h>

int main(void) {
   long int value = get_long("Number: ");
   long int tmp_value = value;
   int position = 1;
   int first_result = 0;
   int first_2_digits = 0;
   int number_of_digits = 0;
   int first_digit = 0;
   while (tmp_value > 0) {
      int digit = tmp_value % 10;
      if (position % 2 == 0) {
         int multiplication = digit * 2;
         if (multiplication > 9) {
               int num2 = multiplication % 10;
               int num1 = (multiplication - num2) / 10;
               first_result += num1;
               first_result += num2;
         } else {
               first_result += multiplication;
         }
      }
      tmp_value /= 10;
      if (tmp_value < 100 && tmp_value > 10) {
         first_2_digits = tmp_value;
      } else if (tmp_value < 10 && tmp_value > 0) {
         first_digit = tmp_value;
      }
      position++;
   }
   position = 1;
   while (value > 0) {
      int digit = value % 10;
      if (position % 2 != 0) {
         first_result += digit;
      }
      value /= 10;
      number_of_digits++;
      position++;
   }
   if (first_result % 10 != 0) {
      printf("INVALID\n");
   } else {
      if ((first_2_digits == 34 && number_of_digits == 15) || (first_2_digits == 37 && number_of_digits == 15)) {
         printf("AMEX\n");
      } else if (first_2_digits >= 51 && first_2_digits <= 55 && number_of_digits == 16) {
         printf("MASTERCARD\n");
      } else if (first_digit == 4 && (number_of_digits == 13 || number_of_digits == 16)) {
         printf("VISA\n");
      } else {
         printf("INVALID\n");
      }
   }
}
