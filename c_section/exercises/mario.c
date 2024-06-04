/**
 * Run in the terminal "make credit" to create the binary code and next Run "./credit" to execute the program.
 * You have to enter a number and a pyramid inspired by super mario block will appear in base of the number you entered
 */
#include <cs50.h>
#include <stdio.h>

int main(void) {
   int value = 0;
   do {
      value = get_int("Height ");
   } while (value < 1 || value > 8);
   for (int i = 1; i <= value; i++) {
      int new_value = i * 2;
      for (int y = value - 1; y >= i; y--) {
         printf(" ");
      }
      for (int j = 1; j<= new_value; j++) {
         printf("#");
         if (j == new_value / 2) {
               printf("  ");
         }
      }
      printf("\n");
    }
}
