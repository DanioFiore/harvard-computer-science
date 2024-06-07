#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check the number of args
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    char *file_name = argv[1];

    // fopen open the input file in read mode "r", with the output assigned to a pointer, which will point to the start of the file
    FILE *pointer_for_file = fopen(file_name, "r");

    if (pointer_for_file == NULL) {
        printf("Error: cannot open %s\n", file_name);
        return 2;
    }

    BYTE buffer[512];

    // Number of images recovered
    int count = 0;

    // Pointer to the file that will be written
    FILE *pointer_for_image = NULL;

    // Name of image
    char filename[8];

    while(fread(buffer, sizeof(BYTE) * 512, 1, pointer_for_file) == 1) {
        if (buffer[0] == 0xFF && buffer[1] == 0xD8 && buffer[2] == 0xFF && (buffer[3]&0xF0) == 0xE0) {
            if (pointer_for_image != NULL) {
                fclose(pointer_for_image);
            }
            sprintf(filename, "%03d.jpg", count++);

            pointer_for_image = fopen(filename, "w");
        }

        if (pointer_for_image != NULL) {
            fwrite(buffer, sizeof(BYTE) * 512, 1, pointer_for_image);
        }
    }
    if (pointer_for_image != NULL) {
        fclose(pointer_for_image);
    }
    fclose(pointer_for_file);
    return 0;
}
