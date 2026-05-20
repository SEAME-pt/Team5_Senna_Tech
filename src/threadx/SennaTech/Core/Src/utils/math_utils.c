#include "utils.h"

UINT stabilizing_two_values(ULONG value1, ULONG value2)
{
    UINT threshold = 3; // cm

    if (value1 > value2 + threshold) 
        return 0;
    else if (value1 < value2 - threshold) 
        return 0;
    else
        return 1; // close enough, snap to target
}
