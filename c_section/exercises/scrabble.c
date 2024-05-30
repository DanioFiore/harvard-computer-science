/**
 * Launch in the terminal "make scrabble" to create the binary code and next launch "./scrabble" to execute the program.
 * You have to enter two word, every character has a value number, the word with the higher value wins!
*/
#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points
int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int calculateScore(string word);

int main(void)
{
   // Prompt the user for two words
   string first_word = get_string("Player 1: ");
   string second_word = get_string("Player 2: ");

   // Calculate the score
   int first_score = calculateScore(first_word);
   int second_score = calculateScore(second_word);

   // Print the winner
   if (first_score > second_score)
   {
      printf("Player 1 wins!\n");
   }
   else if (first_score < second_score)
   {
      printf("Player 2 wins!\n");
   }
   else
   {
      printf("Tie!\n");
   }
}

int calculateScore(string word) {
   int actual_score = 0;

   // Compute score for each character
   for (int i = 0, length = strlen(word); i < length; i++)
   {
      if (isupper(word[i]))
      {
         actual_score += points[word[i] - 'A'];
      }
      else if (islower(word[i]))
      {
         actual_score += points[word[i] - 'a'];
      }
   }

   return actual_score;
}
