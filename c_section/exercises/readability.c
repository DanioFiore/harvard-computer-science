/**
 * Launch in the terminal "make scrabble" to create the binary code and next launch "./scrabble" to execute the program.
 * You have to enter a text and the result will tell you the grade of difficulty of the text!
*/
#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

char sentences[] = {'!', '?', '.'};
size_t sentences_length = sizeof(sentences);
int main(void)
{
   // Prompt the user for some text
   string text = get_string("Text: ");

   // Count the number of letters, words, and sentences in the text
   int number_of_letters = 0;
   int number_of_words = 1;
   int number_of_sentences = 0;
   // Use this bool to check if there is a typo and the user have inserted more than one space or punctuation, if so, don't calculate it as a word or sentence
   bool previous_was_a_space = false;
   bool previous_was_a_sentence = false;
   for (int i = 0, length = strlen(text); i <= length - 1; i++) {
      bool found = false;
      for (int j = 0; j <= sentences_length - 1; j++) {
         if (text[i] == sentences[j]) {
               found = true;
               break;
         }
      }
      if (found) {
         if (!previous_was_a_sentence) {
               number_of_sentences++;
               previous_was_a_sentence = true;
               previous_was_a_space = false;
         }
      }
      if (isalpha(text[i])) {
         number_of_letters++;
         previous_was_a_space = false;
         previous_was_a_sentence = false;
      } else {
         if (text[i] == ' ' && !previous_was_a_space) {
               number_of_words++;
               previous_was_a_space = true;
               previous_was_a_sentence = false;
         }
      }
   }
   // Compute the Coleman-Liau index
   if (number_of_sentences == 0) {
      number_of_sentences++;
   }
   float calc = (0.0588 * number_of_letters / number_of_words * 100) - (0.296 * number_of_sentences / number_of_words * 100) - 15.8;
   int index = round(calc);
   // Print the grade level
   if (index >= 16) {
      printf("Grade 16+\n");
   } else if (index < 1) {
      printf("Before Grade 1\n");
   } else {
      printf("Grade %i\n", index);
   }
}
