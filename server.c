#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
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
    printf(">%s\n", data);
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
	int listen_fd, new_socket ; 
	struct sockaddr_in address; 
	int opt = 1; 
	int addrlen = sizeof(address); 

	char buffer[1024] = {0}; 

	listen_fd = socket(AF_INET /*IPv4*/, SOCK_STREAM /*TCP*/, 0 /*IP*/) ;
	if (listen_fd == 0)  { 
		perror("socket failed : "); 
		exit(EXIT_FAILURE); 
	}
	
	memset(&address, '0', sizeof(address)); 
	address.sin_family = AF_INET; 
	address.sin_addr.s_addr = INADDR_ANY /* the localhost*/ ; 
	address.sin_port = htons(8080); 
	if (bind(listen_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
		perror("bind failed : "); 
		exit(EXIT_FAILURE); 
	} 

	while (1) {
		if (listen(listen_fd, 16 /* the size of waiting queue*/) < 0) { 
			perror("listen failed : "); 
			exit(EXIT_FAILURE); 
		} 

		new_socket = accept(listen_fd, (struct sockaddr *) &address, (socklen_t*)&addrlen) ;
		if (new_socket < 0) {
			perror("accept"); 
			exit(EXIT_FAILURE); 
		}

		char msg[100];
		recv_message(new_socket, msg) ;

                if(atoi(msg)==2) {
			printf("OK\n");
			system("docker cp ./hw1-MJ/main.c client:.");
		}
		printf(">>%s\n", msg) ;

		send_message(new_socket, "3") ;	
		shutdown(new_socket, SHUT_WR) ;
	}
}
