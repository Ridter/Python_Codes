/*************************************************************************
	> File Name: main.c
	> Author: wz
	> Created Time: Mon 18 Nov 2013 10:22:08 PM CST
 ************************************************************************/

#include<stdio.h>
#include<sys/types.h>
#include<unistd.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<string.h>
#include<stdlib.h>
#include<time.h>


#include "packet.h"
#include "md5.h"


extern char user_name[32];
extern char pass_word[32];
extern struct ipclient_packet_t packet;


typedef struct sockaddr SA;

struct sockaddr_in client_addr1;
struct sockaddr_in client_addr2;

struct sockaddr_in server_addr1;
struct sockaddr_in server_addr2;


int client_socket_1;
int client_socket_2;


void conect_config()
{
	struct timeval tv;
	socklen_t addr_len = sizeof(SA);

	tv.tv_sec = 5;
	tv.tv_usec = 0;


	client_socket_1 = socket(AF_INET,SOCK_DGRAM,0);
	client_socket_2 = socket(AF_INET,SOCK_DGRAM,0);

	client_addr1.sin_family = AF_INET;
	client_addr1.sin_addr.s_addr = htons(INADDR_ANY);
	client_addr1.sin_port = htons(5200);

	server_addr1.sin_family = AF_INET;
	server_addr1.sin_addr.s_addr = inet_addr(SERVER_IP);
	server_addr1.sin_port = htons(5300);

	client_addr2.sin_family = AF_INET;
	client_addr2.sin_addr.s_addr = htons(INADDR_ANY);
	client_addr2.sin_port = htons(5201);

	server_addr2.sin_family = AF_INET;
	server_addr2.sin_addr.s_addr = inet_addr(SERVER_IP);
	server_addr2.sin_port = htons(5301);


	bind(client_socket_1,(SA *)&client_addr1,sizeof(SA));
	setsockopt(client_socket_1,SOL_SOCKET,SO_RCVTIMEO,(const char *)&tv,sizeof(struct timeval));

	bind(client_socket_2,(SA *)&client_addr2,sizeof(SA));
	setsockopt(client_socket_2,SOL_SOCKET,SO_RCVTIMEO,(const char *)&tv,sizeof(struct timeval));
	
	

}

int open_ip()
{
	socklen_t addr_len;
	
	build_0x1f();
	sendto(client_socket_1,packet.data,300,0,(SA *)&server_addr1,sizeof(server_addr1));

	reset();
	recvfrom(client_socket_1,packet.data,300,0,NULL,NULL);
	recv_0x20();

	build_0x21();
	sendto(client_socket_1,packet.data,300,0,(SA *)&server_addr1,sizeof(server_addr1));
	
	reset();
	recvfrom(client_socket_1,packet.data,300,0,NULL,NULL);
	recv_0x22();


}

int main(int argc,char *argv[])
{
	

	printf("请输入帐号：");
	scanf("%s",user_name);
	printf("请输入密码:");
	scanf("%s",pass_word);

	conect_config();
	open_ip();
	
	while(1)
	{
		build_0x1e();
		sendto(client_socket_2,packet.data,500,0,(SA *)&server_addr2,sizeof(server_addr2));

		reset();
		recvfrom(client_socket_2,packet.data,sizeof(packet.data),0,NULL,NULL);
		recv_0x1f();

		sleep(30);
	}
	

}
