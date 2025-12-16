#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
    float speed = atof(argv[1]);
    printf("Speed read: %.2f\n", speed);

    if (speed < 0 || speed > 180) {
        printf("FAULT: speed out of valid range\n");
    } else {
        printf("Speed OK\n");
    }

    return 0;
}
