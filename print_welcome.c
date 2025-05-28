#include <stdio.h>

void print_welcome() {
    printf("Hello, world! (%s)",
#ifdef __clang__
        "clang"
#else
        "gcc"
#endif
    );
}