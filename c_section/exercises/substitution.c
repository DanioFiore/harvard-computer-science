/**
 * Launch in the terminal "make scrabble" to create the binary code and next launch "./scrabble [key]" to execute the program.
 * You have to enter the key that the program will use to encrypt your next plaintext!
*/
#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[]) {
   // catch the command line arg
   string key = argv[1];
   // exit if are more or less than one key
   if (argc != 2) {
      printf("The program accept only one key\n");
      return 1;
   }
   // exit if contains less than 26 char
   if (strlen(key) != 26) {
      printf("The key must contain exactly 26 char\n");
      return 1;
   }
   // exit if one char is repeated
   for (int i = 0; i <= strlen(key) - 1; i++) {
      // exit if are not alphabetical
      if (!isalpha(key[i])) {
         printf("The key must be alphabetical\n");
         return 1;
      }
      for (int j = 0; j <= strlen(key) - 1; j++) {
         if (i == j) {
               continue;
         }
         if (key[i] == key[j]) {
               printf("The key must contain unique char\n");
               return 1;
         }
      }
   }
   // ask for the plaintext
   string plaintext = get_string("plaintext: ");
   // loop through the plaintext and the key to substitute
   char ciphertext[256] = "";
   for (int i = 0; i <= strlen(plaintext) - 1; i++) {
      // subsitute with the corresponding position of the key and transform it to lower or uppercase after check the corresponding alphabetical position
      if (plaintext[i] == ' ') {
         ciphertext[i] = ' ';
      } else if (isupper(plaintext[i])) {
         char actual_char = key[plaintext[i] - 'A'];
         ciphertext[i] = toupper(actual_char);
      } else if (islower(plaintext[i])) {
         char actual_char = key[plaintext[i] - 'a'];
         ciphertext[i] = tolower(actual_char);
      } else {
         ciphertext[i] = plaintext[i];
      }
   }

   printf("ciphertext: %s\n", ciphertext);
   return 0;
}
