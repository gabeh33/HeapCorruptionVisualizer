#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main() {
	printf("============ Demonstrating the nature of fastbins ================\n");
	int size = 22;
	printf("Allocating buffers a-d of size %i\n", size);
	char *a = malloc(size);  
	char *b = malloc(size); 
	char *c = malloc(size);
	char *d = malloc(size);
	char *e = malloc(size);
	char *f = malloc(size);
	char *g = malloc(size);
	char *h = malloc(size);
	char *i = malloc(size);

	printf("a points to: %p\n", a);
	printf("b points to: %p\n", b);
	printf("c points to: %p\n", c);
	printf("d points to: %p\n\n", d);
	
	printf("Freeing pointers a-d...\n\n");

	free(a);
	free(b);
	free(c);
	free(d);
	free(e);
	free(f);
	free(g);
	free(h);
	free(i);

	printf("Re-allocating memory of size %i to a-d\n", size);
	a = malloc(size);     
	b = malloc(size);    
	c = malloc(size);   
	d = malloc(size); 

	printf("a points to: %p\n", a);
	printf("b points to: %p\n", b);
	printf("c points to: %p\n", c);
	printf("d points to: %p\n", d);
	return 0;

}
