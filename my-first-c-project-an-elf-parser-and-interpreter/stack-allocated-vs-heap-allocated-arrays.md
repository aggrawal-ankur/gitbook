# Stack Allocated vs Heap Allocated Arrays

Normal arrays are stack-allocated. Their lifecycle is the lifecycle of the block that contains them. Therefore, they can't be used for returning something. Stack overflow might also happen.

A dynamically allocated array, or a heap-allocated array is accessible until it is manually freed. It is perfect for returning structs.
