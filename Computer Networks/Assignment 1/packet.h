#include <stdint.h>

typedef struct pkt
{
	int pkt_size;
	int seq_num;
	int RC;
	uint64_t  timestamp;	
} packet;
