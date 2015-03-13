/*************************************************************************
	> File Name: packet.h
	> Author: wz
	> Created Time: Sat 16 Nov 2013 10:25:29 AM CST
 ************************************************************************/

#ifndef _PACKET_H
#define _PACKET_H

#define SERVER_IP "172.16.12.11"

#define CONSTANT_1 0x0a
#define CONSTANT_2 0x0d10
#define CONSTANT_3 0x05
#define CONSTANT_4 0x05dc
#define CONSTANT_5 0x0f
#define CONSTANT_6 0x2382


struct send_data_t
{
	unsigned int data_len;
	char data[100];

};

struct ipclient_packet_head_t
{
	unsigned short sign;//ipclient标志
	unsigned char number;//数据包序号
	char unknow[8]; //似乎恒为0

};

struct ipclient_packet_t
{
	char *current;
	char data[500];

};

void ipclient_packet_init();
void add_data(void *,int );
void set_point(int );
void fill_with_0x00(int );
void reset();


int MD5(unsigned char *out,unsigned char *in);
int hex_to_str(char *str,char *hex,int len);
int generate_md5_string(char *str);


//连接服务器函数
void build_0x05();

int recv_0x06();


//开放IP函数

void build_0x1f();
void recv_0x20();
void build_0x21();
void recv_0x22();


//心跳包函数
void build_0x1e();
void recv_0x1f();


//关闭IP函数
void build_0x14();
void recv_0x15();
void build_0x16();
void recv_0x17();

#endif
