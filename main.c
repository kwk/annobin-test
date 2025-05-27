#include <stdio.h>

int main(int argc, char* argv[]) {
    printf("Hello, world! (%s)",
#ifdef __clang__
        "clang"
#else
        "gcc"
#endif
    );    
    return 0;
}