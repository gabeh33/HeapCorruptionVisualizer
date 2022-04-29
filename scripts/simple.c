#include <stdio.h>

int main() {
	printf("Mallocing 50 bytes\n");
	char* first_malloc = (char *)malloc(50);
	char* second_malloc = (char*)malloc(55);
	printf("Freeing those 50 bytes\n");
	free(second_malloc);
	
	return 0;

}
