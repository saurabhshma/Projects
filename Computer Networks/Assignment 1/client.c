#include "packet.h"
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>
#include <errno.h>
#include <sys/time.h>
#define PORT "4951"

int main(int argc, char *argv[])
{
	int c;
	while((c = getopt(argc, argv, "h")) != -1) //Print Usage
	{
		switch(c)
		{
			case 'h':
				printf("`:Usage: client Packet_Size RC_value Output_file IP_Address_of_echo\n");
				exit(1);
			default:
				;
		}
	}

	struct addrinfo init, *echoinfo, *i, *j;
	int gai_status, sock_des, num_bytes;
	socklen_t addr_len;
	struct sockaddr_storage from;
	int temp = atoi(argv[1]);
	//int packet_size = atoi(argv[1]);
	int yes = 1;
	
	memset(&init, 0, sizeof(init)); //Initialise Addrinfo structure
	init.ai_family = AF_UNSPEC;
	init.ai_socktype = SOCK_DGRAM; 	
	
	if((gai_status = getaddrinfo(argv[4], PORT, &init, &echoinfo)) != 0) //Get address information of echo
	{
		fprintf(stderr, "getaddrinfo() error: %s\n", gai_strerror(gai_status));
		exit(1);
	}
	for(i = echoinfo; i != NULL; i = i->ai_next) //Find the working socket from the linked list of getaddrinfo results
	{
		j = i;
		if((sock_des = socket(i->ai_family, i->ai_socktype, i->ai_protocol)) == -1)
		{
			perror("client: socket");
			continue;
		}
			break;
	}
	
	if(i == NULL) //if no socket initialised, exit
	{
		fprintf(stderr, "client: failed to create socket\n");
		exit(1);
	}
	freeaddrinfo(echoinfo);
	setsockopt(sock_des, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)); //reuse the port of if any socket is connected previously at that port
	/*if((num_bytes = sendto(sock_des, &packet_size, sizeof(int), 0, i->ai_addr, i->ai_addrlen)) == -1) //send packet size to echo
	{
	perror("client: sendto");
	exit(1);
	}*/
	int x;
	struct timeval start, end;
	unsigned long int time_diff;
	FILE *fp;
	if((fp = fopen(argv[3], "a+")) == NULL)
	{
		fprintf(stderr, "File cannot be opened\n");
		exit(1);
	}
	int packet_size;
	for(packet_size = 100; packet_size <= 1000; packet_size +=  100)
	{
		packet *msg = (packet *) malloc(packet_size);
		for(x = 0; x < 50; x++)
		{
			struct timeval timer;
			timer.tv_sec = 2;
			timer.tv_usec = 0;
			fd_set readfds; 
			FD_ZERO(&readfds);
			FD_SET(sock_des, &readfds);
			msg->RC = atoi(argv[2]);
			msg->seq_num = x + 1;
			msg->pkt_size = packet_size;
			gettimeofday(&start, 0); 
			msg->timestamp = start.tv_sec*(uint64_t)1000000 + start.tv_usec; //add timestamp
			while(msg->RC != 0) //While reflection count not equal to 0 keep sending packet
			{
				if((num_bytes = sendto(sock_des, msg, packet_size, 0, i->ai_addr, i->ai_addrlen)) == -1) //send data
				{
					perror("client: sendto");
					exit(1);
				}
				addr_len = sizeof (from);
				select(sock_des + 1, &readfds, NULL, NULL, &timer);  //add timer to the packet
rcv_nxt: 				if(FD_ISSET(sock_des, &readfds))
				{
					if((num_bytes = recvfrom(sock_des, msg, packet_size, 0, (struct sockaddr *)&from, &addr_len)) == -1) //receive data
					{
						perror("client: recvfrom");
						exit(1);
					}
					if(msg->seq_num != x + 1) //if sequence number doesn't match jump to receive next packet
						goto rcv_nxt;
				}
					else
					{
						printf("Packet Loss! Packet_size: %d Seq_Num: %d\n", msg->pkt_size, msg->seq_num);
						goto skip;
					}
				(msg->RC)--; //Decrease reflection count
			}

			gettimeofday(&end, 0);
			time_diff = (end.tv_sec*(uint64_t)1000000 + end.tv_usec) - msg->timestamp; //find Cumulative RTT
			fprintf(fp, "%d %ld\n", packet_size, time_diff);  //print to file
skip:
			;
		}
		free(msg);
	}
	close(sock_des);
	fclose(fp);
	return 0;
}
