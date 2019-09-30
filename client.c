#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

void
recv_message(int conn, char * buf)
{   
    int s, len ;
//    char buf[1024] ;
    char * data = 0x0 ;
    len = 0 ;
    
    while ( (s = recv(conn, buf, 1023, 0)) > 0 ) {
        buf[s] = 0x0 ;
        if (data == 0x0) {
            data = strdup(buf) ;
            len = s ;
        }
        else {
            data = realloc(data, len + s + 1) ;
            strncpy(data + len, buf, s) ;
            data[len + s] = 0x0 ;
            len += s ;
        }
     
    }
//    printf(">%s\n", data);
}

void
send_message(int conn, char * buffer)
{   
    char * data; 
    data = (char *)malloc(sizeof(char)*(strlen(buffer)+1)) ;
    strcpy(data, buffer);
    int len ;
    len = strlen(data) ;
    int s = 0 ;
    while (len > 0 && (s = send(conn, data, len, 0)) > 0) {
        data += s ;
        len -= s ;
    }
}
int
main(int argc, char const *argv[])
{
        struct sockaddr_in serv_addr;
        int sock_fd ;
        int s, len ;
        char buffer[1024] = {0};
        char * data ;

        sock_fd = socket(AF_INET, SOCK_STREAM, 0) ;
        if (sock_fd <= 0) {
                perror("socket failed : ") ;
                exit(EXIT_FAILURE) ;
        }

        memset(&serv_addr, '0', sizeof(serv_addr));
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(8080);
        if (inet_pton(AF_INET, "222.239.251.48", &serv_addr.sin_addr) <= 0) {
                perror("inet_pton failed : ") ;
                exit(EXIT_FAILURE) ;
        }

        if (connect(sock_fd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {
                perror("connect failed : ") ;
                exit(EXIT_FAILURE) ;
        }

//        scanf("%s", buffer) ;
//        data = buffer ;
        data = "2" ; //connect success and give me repo
        send_message(sock_fd, data);

        shutdown(sock_fd, SHUT_WR) ;

        char recv_data[100] ;
        recv_message(sock_fd, recv_data) ;
	printf(">%s\n", recv_data);

	if(atoi(recv_data) != 3) {
		printf("====ERROR:No HW_FILE====") ;
	}

	system("gcc main.c") ;
	system("./a.out") ;

	
}
