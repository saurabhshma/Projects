#include <sys/time.h>
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

#define PORT "4951"

int main(int argc, char *argv[])
{
	int c;
	while((c = getopt(argc, argv, "h")) != -1) //print Usage
	{
		switch(c)
		{
			case 'h':
				printf("Usage: echo\n");
				exit(1);
			default:
				;
		}
	}
	int yes = 1;
	struct addrinfo init, *echoinfo, *i, *j;
	int gai_status, sock_des, num_bytes;
	struct sockaddr_storage from;
	socklen_t addr_len;

	memset(&init, 0, sizeof(init));  //Initialise Addrinfo structure
	init.ai_family = AF_UNSPEC;
	init.ai_socktype = SOCK_DGRAM;
	init.ai_flags = AI_PASSIVE;

	if((gai_status = getaddrinfo(NULL, PORT, &init, &echoinfo)) != 0) //get address information of the client
	{
		fprintf(stderr, "getaddrinfo() error: %s\n", gai_strerror(gai_status));
		exit(1);
	}
	
	for(i = echoinfo; i != NULL; i = i->ai_next) ////Find the working socket from the linked list of getaddrinfo results
	{
		j = i;
		if((sock_des = socket(i->ai_family, i->ai_socktype, i->ai_protocol)) == -1)
		{
			perror("echo: socket");
		}
		else
			break;
	}

	if(i == NULL) //if no socket initialised, exit
	{
		fprintf(stderr, "echo: failed to create socket\n");
		exit(1);
	}
	setsockopt(sock_des, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)); //reuse the port if any socket is connected previously used at that port
	if(bind(sock_des, j->ai_addr, j->ai_addrlen) == -1) //bind socket to the port
	{
		close(sock_des);
		perror("echo: bind");
		exit(1);
	}
	freeaddrinfo(echoinfo);
	addr_len = sizeof from;
	/*if((num_bytes = recvfrom(sock_des, &packet_size, sizeof(int), 0, (struct sockaddr *)&from, &addr_len)) == -1) //receive packet size
	{
		perror("echo: recvfrom");
		exit(1);
	}
	packet *msg = (packet *) malloc(packet_size);*/
	packet *msg = (packet *) malloc(1000);
	packet *realloc_msg;
	int packet_size = 1000;
	int count = 1;
	addr_len = sizeof(from);
	while(1)
	{	
		if((num_bytes = recvfrom(sock_des, msg, packet_size, 0, (struct sockaddr *)&from, &addr_len)) == -1) //receive data
		{
			perror("echo: recvfrom");
			exit(1);
		}
		if(packet_size != msg->pkt_size)
		{
			packet_size = msg->pkt_size;
			realloc_msg = realloc(msg, packet_size);
			if(realloc_msg)
				msg = realloc_msg;
			else
			{	
				fprintf(stderr, "Realloc Failed\n");
				exit(1);
			}
		}
		(msg->RC)--;
		printf("Packet_Received! Packet_size: %d, Seq_num: %d, RC: %d\n", packet_size, msg->seq_num, msg->RC);
		if((num_bytes = sendto(sock_des, msg, packet_size, 0, (struct sockaddr *)&from, addr_len)) == -1) //send the packet back
		{
			perror("echo: sendto");
			exit(1);
		}
	}
	close(sock_des);
	free(msg);
	return 0;
}
