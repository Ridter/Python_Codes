/*************************************************************************
	> File Name: packet.c
	> Author: wz
	> Created Time: Sat 16 Nov 2013 10:39:07 AM CST
 ************************************************************************/
#include<string.h>
#include<stdlib.h>
#include<stdio.h>
#include<netinet/in.h>


#include "packet.h"
#include "md5.h"
unsigned char mac[6] = {0xb8,0x70,0xf4,0xff,0x6e,0xa6};

unsigned char temp1[] = {0x21,0x40,0x23,0x24,0x25,0x25,0x5e,0x26,0x2a,0x28,0x29};

unsigned char temp2[] = {0x71,0x77,0x65,0x72,0x74,0x79,0x75,0x39,0x30};

unsigned char temp3[] = {0x41,0x53,0x44,0x46,0x47,0x48};
unsigned char temp4[] = {0x39,0x67,0x64,0x74,0x34,0x33,0x37,0x34,0x35,0x77,0x72,0x77,0x71,0x72};

unsigned char temp5[] = {0x31,0x31,0x3a,0x32,0x32,0x3a,0x33,0x33,0x3a,0x34,0x34,0x3a,0x35,0x35,0x3a,0x36,0x36,0x2d,0x1f,0xd6,0x03,0xcc,0xf2,0x24};

unsigned char temp6[] = {0x71,0x77,0x65,0x72,0x74,0x79,0x75,0x69,0x6f,0x70};

//unsigned char temp7[] = {0xe4,0x3e,0x86};

//unsigned char temp8[] = {0x5c,0x8f,0xc2,0xf5,0xf0,0xa9,0xdf,0x40};

//unsigned char temp9[] = {0x31,0x31,0x30,0x30,0x33,0x36,0x30,0x32,0x30,0x31};

//unsigned char temp10[] = {0x53,0x70,0x69,0x64,0x65,0x72,0x6d,0x61,0x6e};


unsigned char open_succeed[] = {0xbf,0xaa,0xb7,0xc5,0x49,0x50,0xb3,0xc9,0xb9,0xa6};


char user_name[32];
char pass_word[32];

unsigned short key;
unsigned int counter;

struct ipclient_packet_t packet;
struct ipclient_packet_head_t head;

void ipclient_packet_init()
{
	memset(packet.data,0,500);
	packet.current = packet.data;
}

void add_data(void *buffer,int len)
{
	memcpy(packet.current,buffer,len);
	packet.current += len;
}

void set_point(int move)
{
	packet.current += move;
}

void fill_with_0x00(int n)
{
	while(&packet.data[n-1] != packet.current)
	{
		*packet.current = (char )0x00;
		 packet.current ++;
	}

	*packet.current = (char)0x00;
}

void reset()
{
	memset(packet.data,0,500);
	packet.current = packet.data;
}

int MD5(unsigned char *out,unsigned char *in)
{
	MD5_CTX mctx;
	MD5Init(&mctx);
	MD5Update(&mctx,in,strlen((char *)in));
	MD5Final(&mctx,out);

	return 0;
}

int hex_to_str(char *str,char *hex,int len)
{
	int i;

	for(i = 0; i < len; i++)
		sprintf(str + i*2,"%02X",(unsigned char)hex[i]);

	return 0;

}

int generate_md5_string(char *str)  //用户名和密码加密
	//存于str中
{
	char sz_str[64];
	char sz_md5[64];

	memset(sz_str,0x00,sizeof(sz_str));
	sprintf(sz_str,"%d",key - CONSTANT_2);

	strcat(sz_str,pass_word);

	memset(sz_md5,0x00,sizeof(sz_md5));
	MD5((unsigned char *)sz_md5,(unsigned char *)sz_str);
	
	memset(sz_str,0x00,sizeof(sz_str));
	hex_to_str(sz_str,sz_md5,0x10);

	memset(sz_md5,0x00,sizeof(sz_md5));
	strcpy(sz_md5,sz_str);

	memset(sz_str,0x00,sizeof(sz_str));
	strncpy(sz_str,sz_md5,CONSTANT_3);
	strcat(sz_str,user_name);

	MD5((unsigned char *)sz_md5,(unsigned char *)sz_str);
	memset(sz_str,0x00,sizeof(sz_str));
	hex_to_str(sz_str,sz_md5,0x10);

	memcpy(str,sz_str,strlen(sz_str));

	return 0;
}



void build_0x1f()
{
	int i;
	
	reset();

	head.sign = htons(0x8223);
	head.number = 0x1f;
	memset(&head.unknow,0,8);
	add_data(&head,11);


	struct send_data_t send_data;
	send_data.data_len = strlen(user_name);  //0a
	send_data.data_len<<24;

	//每个用户名减去0x0a
	for(i = 0; i < strlen(user_name); i++)
		send_data.data[i] = user_name[i] - CONSTANT_1;

	add_data(&send_data,4+strlen(user_name));

	send_data.data_len = 0x0b;
	send_data.data_len<<24;
	strcpy(send_data.data,temp1);
	add_data(&send_data,4+sizeof(temp1));
	
	send_data.data_len = 0x07;
	send_data.data_len<<24;
	strcpy(send_data.data,temp2);
	add_data(&send_data,4+sizeof(temp2));
	packet.data[packet.current-&packet.data[0]] = 0x00;
	set_point(1);
	packet.data[packet.current-&packet.data[0]] = 0x00;
	set_point(1);


	send_data.data_len = 0x01;
	send_data.data_len<<24;
	add_data(&send_data,4);

	send_data.data_len = 0x06;
	send_data.data_len<<24;
	strcpy(send_data.data,temp3);
	add_data(&send_data,4+sizeof(temp3));

	fill_with_0x00(300);

}

void recv_0x20()
{
	char *p = packet.data;
	unsigned char ch;
	p += 51;

	key = *((unsigned short *)(p));

}


void build_0x21()
{
	int i;
	char md5[32];
	struct send_data_t send_data;

	reset();

	head.number = 0x21;
	memset(&head.unknow,0,8);
	add_data(&head,11);


	send_data.data_len = 0x0e;
	send_data.data_len<<24;
	strcpy(send_data.data,temp4);
	add_data(&send_data,4 + sizeof(temp4));

	send_data.data_len = 0x1e;
	send_data.data_len<<24;
	add_data(&send_data,4);
	

	generate_md5_string(md5);//加密
	add_data(&md5,0x1e);

	send_data.data_len = 0x11;
	send_data.data_len<<24;
	strcpy(send_data.data,temp5);
	add_data(&send_data,4 + sizeof(temp5));


	send_data.data_len = 0x0a;
	packet.data[packet.current-&packet.data[0]] = 0x00;
	set_point(1);
	send_data.data_len<<16;
	strcpy(send_data.data,temp6);
	add_data(&send_data,4 + sizeof(temp6));

	
	fill_with_0x00(300);

}

void recv_0x22()
{
	char *p = packet.data;
	unsigned char ch[30];
	char *finish;
	int i = 0;
	p += 0x02;

	if(0x22 != *p)
	{
		printf("IP开放失败.\n");

		return ;
	}

	p += 98;
	finish = p+10;
	while(p <= finish)
	{
		ch[i] = *p;
		p++;
		i++;
	}
	ch[i] = 0;

	if(strcmp(ch,open_succeed) == 0)
	{
		printf("IP开放成功.\n");

	}
	else
	{
		
		printf("IP开放失败.\n");
	}

}

void build_0x1e()
{
	int i;
	unsigned short identity;
	double number;
	struct send_data_t send_data;
	unsigned char t7[] = {0xe4,0x3e,0x86};

	unsigned char t8[] = {0x5c,0x8f,0xc2,0xf5,0xf0,0xa9,0xdf,0x40};

	unsigned char t9[] = {0x31,0x31,0x30,0x30,0x33,0x36,0x30,0x32,0x30,0x31};

	unsigned char t[] = {0x53,0x70,0x69,0x64,0x65,0x72,0x6d,0x61,0x6e};

	reset();
	
	head.sign = htons(0x8223);
	head.number = 0x1e;

	identity = key - CONSTANT_2 + CONSTANT_4;
	
	memcpy(head.unknow,&identity,2);
	memset(&head.unknow[2],0,6);
	add_data(&head,11);

	add_data(t7,3);

	send_data.data_len = 0x0a;
	send_data.data_len<<24;
	strcpy(send_data.data,t8);
	add_data(&send_data,4 + sizeof(t8));

	send_data.data_len = 0x09;
	send_data.data_len<<24;
	strcpy(send_data.data,t9);
	add_data(&send_data,4 + sizeof(t9));

	fill_with_0x00(500);

}



void recv_0x1f()
{
	double flow = 0;
	double balance = 0;
	char *p = packet.data;

	p += 0x02;
	if(0x1f != *p)
		return;

	p += 0x09;
	memcpy(&flow,p,0x08);
	p += 0x08;
	memcpy(&balance,p,0x08);

	p += 0x08;

	printf("当前流量:%4.2lf k\n",flow);
	printf("剩余金额:%4.2lf 元\n",balance);


}


