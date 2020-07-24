// Server side implementation of UDP client-server model 
#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <netinet/in.h> 
  
#define PORT 8080 
#define MAXLINE 17

int main() { 
    int sockfd; 
    char buffer[MAXLINE]; 
    char *hello = "Hello from server"; 
    struct sockaddr_in servaddr, cliaddr; 
      
    // Creating socket file descriptor 
    if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) { 
        perror("socket creation failed"); 
        exit(EXIT_FAILURE); 
    } 
      
    memset(&servaddr, 0, sizeof(servaddr)); 
    memset(&cliaddr, 0, sizeof(cliaddr)); 
      
    // Filling server information 
    servaddr.sin_family    = AF_INET; // IPv4 
    servaddr.sin_addr.s_addr = INADDR_ANY; 
    servaddr.sin_port = htons(PORT); 
      
    // Bind the socket with the server address 
    if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) { 
        perror("bind failed"); 
        exit(EXIT_FAILURE); 
    } 

    int len = sizeof(cliaddr); 

    recvfrom(sockfd, (char*)buffer, MAXLINE, 0, (struct sockaddr*) &cliaddr, (socklen_t*) &len); 

    //buffer[n] = '\0'; 
    //printf("Client : %s\n", buffer); 
    //printf("Client port is: %d\n", htons(cliaddr.sin_port));
    
    int message_size = ntohs(cliaddr.sin_port);
    char hidden_message[message_size+1];
    memset(&hidden_message, 0, message_size+1); 

    for(int n =0; n < message_size; n++) {
    	recvfrom(sockfd, buffer, MAXLINE, 0, (struct sockaddr*) &cliaddr, (socklen_t*) &len); 
    	hidden_message[n] = ntohs(cliaddr.sin_port);
    	printf("%d - Client port: %d \n", n, ntohs(cliaddr.sin_port)); 
    }

    close(sockfd);
    printf("Client : %s\n", hidden_message); 

    return 0; 
} 