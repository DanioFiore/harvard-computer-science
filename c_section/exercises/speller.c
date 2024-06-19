/**
 * My solution to CS60 Speller exercise. This solution is valid for the dictionary.c file
 */
// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

unsigned int hash_val;
unsigned int counter;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    hash_val = hash(word);

    for (node *cursor = table[hash_val]; cursor != NULL; cursor = cursor->next) {
        if (strcasecmp(word, cursor->word) == 0) {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned long tot = 0;

    for (const char *ptr = word; *ptr != '\0'; ptr++) {
        tot += tolower(*ptr);
    }

    return tot % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (file == NULL) {
        printf("Unable to open %s\n", dictionary);
        return false;
    }

    char word[LENGTH + 1];

    while (fscanf(file, "%s", word) != EOF) {
        node *n = malloc(sizeof(node));
        if (n == NULL) {
            fclose(file);
            return false;
        }

        strcpy(n->word, word);

        hash_val = hash(word);
        n->next = table[hash_val];
        table[hash_val] = n;
        counter++;
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (counter > 0) {
        return counter;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++) {
        node *cursor = table[i];
        while (cursor) {
            node *tmp_var = cursor;
            cursor = cursor->next;
            free(tmp_var);
        }
    }
    return true;
}
