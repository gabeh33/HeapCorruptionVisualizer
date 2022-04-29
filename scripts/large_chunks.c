#include <stdio.h>
#include <stdlib.h>
int main(){
	int* large_1 = (int*) malloc(2048);

	free(large_1);
	char* large_4 = (char*)malloc(1100);
	free(large_4);
	char* large_2 = malloc(5000);
	char* large_3 = malloc(8000);
	free(large_2);
	free(large_3);
	char* catch = malloc(10);
	free(catch);
	char* rand = malloc(500);
	return 0;
}
