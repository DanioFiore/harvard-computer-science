#include <cs50.h>
#include <stdio.h>

int main(void)
{
   string answer = get_string("What's your name? ");
   printf("Hello, %s\n", answer);
}

// To compile with cs50 lib, after installation (https://github.com/cs50/libcs50) use the following command: gcc -o hello hello.c -lcs50