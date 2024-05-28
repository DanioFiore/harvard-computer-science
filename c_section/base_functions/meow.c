#include <stdio.h>
#include <cs50.h>

void meow(int n);

int main(void)
{
   meow(3);
}

// Meow some number of times
void meow(int n)
{
   for (int i = 0; i < n; i++)
   {
      printf("meow\n");
   }
}