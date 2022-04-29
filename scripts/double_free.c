#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main() {
	printf("============ Simple double free  ================\n");
	int size = 50;
	printf("Allocating buffers a-c of size %i\n", size);
	char *a = malloc(size);  
	char *b = malloc(size); 
	char *c = malloc(size);

	printf("a points to: %p\n", a);
	printf("b points to: %p\n", b);
	printf("c points to: %p\n\n", c);
	
	printf("Freeing pointers a, b, c, a!!\n"); 

	free(a);
	free(b);
	free(c);
	free(a);
	
	char* d;
	char* e;
	char* f;

	printf("Re-allocating memory of size %i to d-f\n", size);
	d = malloc(size);     
	e = malloc(size);    
	f = malloc(size);   

	printf("d points to: %p\n", d);
	printf("e points to: %p\n", e);
	printf("f points to: %p\n", f);
	return 0;

}
