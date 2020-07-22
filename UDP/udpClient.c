// Client side implementation of UDP client-server model 
#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/types.h> 
#include <sys/socket.h>
#include <arpa/inet.h> 
#include <netinet/in.h> 
#include <sys/types.h>

#define DST_PORT 8080 
#define SRC_PORT 3333 
#define MAXLINE 1024 


int string_to_bytes(char *message, int message_len, int *bytes) {
    for(int i = 0; i < message_len; i++) {
        bytes[i] += message[i];
    }
    return 0;
}

int bind_socket(int sockfd, struct sockaddr *srcaddr, int srcaddr_size) {
    if (bind(sockfd, srcaddr, srcaddr_size) < 0) {
        perror("bind");
        exit(1);
    }
    return 0;
}


int main() { 
    int sockfd; 
    char *hello = "Hello from client"; 
    char secret_message[25] = "This is my secret message"; 
    int secret_message_len = 25;//strlen(secret_message);
    int secret_message_bytes_buffer[secret_message_len];
    
    memset(&secret_message_bytes_buffer, 0, secret_message_len); 
    string_to_bytes(secret_message, secret_message_len, secret_message_bytes_buffer);

    struct sockaddr_in servaddr, srcaddr; 

    // Creating socket file descriptor 
    if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) { 
        perror("socket creation failed"); 
        exit(EXIT_FAILURE); 
    } 

    memset(&servaddr, 0, sizeof(servaddr)); 
    
    // Filling server information 
    servaddr.sin_family = AF_INET; 
    servaddr.sin_port = htons(DST_PORT); 
    servaddr.sin_addr.s_addr = INADDR_ANY; 

    memset(&srcaddr, 0, sizeof(srcaddr));
    srcaddr.sin_family = AF_INET;
    srcaddr.sin_addr.s_addr = htonl(INADDR_ANY);

    // First send secret message length:
    // Set desired source port in UDP datagram!!
    srcaddr.sin_port = htons(secret_message_len); 
    bind_socket(sockfd, (struct sockaddr *)&srcaddr, sizeof(srcaddr));
    sendto(sockfd, (const char *)hello, strlen(hello), 0, (const struct sockaddr *) &servaddr, sizeof(servaddr)); 
    close(sockfd); 

    //printf("Print secret message bytes buffer");
    for (int i = 0; i < secret_message_len; i++) {
        printf("Letter %c is %d\n", secret_message[i], secret_message_bytes_buffer[i]);
    }

    for (int i = 0; i < secret_message_len; i++) {
        srcaddr.sin_port = secret_message_bytes_buffer[i]; 
        if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) { 
            perror("socket creation failed"); 
            exit(EXIT_FAILURE); 
        } 
        bind_socket(sockfd, (struct sockaddr *)&srcaddr, sizeof(srcaddr));
        sendto(sockfd, (const char *)hello, strlen(hello), 0, (const struct sockaddr *) &servaddr, sizeof(servaddr)); 
        //printf("Hello message sent from port %d.\n", secret_message_bytes_buffer[i]);
        close(sockfd);
    }

    printf("Close client socket.\n");
    return 0; 
} 
