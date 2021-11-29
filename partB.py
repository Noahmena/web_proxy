from socket import *

# create server socket
serverPort = 80
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((gethostbyname(gethostname()), serverPort))
serverSocket.listen(1)

while True:
    # begin receiving data from client
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print('Received a connection from:', addr)
    sentence = connectionSocket.recv(1024)
    print(sentence)
    # get filename from sentence
    print(sentence.split()[1])
    filename = sentence.decode().split()[1].partition("//")[2]
    filenameEnd = filename.partition("/")[2]
    # ignore favicon.ico requests (caused problems)
    if filenameEnd == "favicon.ico":
        continue
    print(filename)
    fileExist = "false"
    if filename.split("/") == "":
        filename2 = "/" + filename.replace('/', '', 1)
    else:
        filename2 = "/" + filename
    try:
        # check if file exists
        f = open(filename2[1:], "rb")
        outputdata = f.readlines()
        fileExist = "true"
        # send response
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type:text/html\r\n".encode())
        response = "".encode()
        for x in outputdata:
            response += x
        connectionSocket.send(response)
        print('Read from cache')

    except IOError as e:
        # if file is not found, create file
        print(e)
        if fileExist == "false":
            # create proxy server socket
            proxySocket = socket(AF_INET, SOCK_STREAM)  # fill in
            if filename.split("/") == "":
                temp = filename.replace("/", "", 2)
            else:
                temp = filename
            hostName = temp.split("/")[0].partition("/")[0]
            print(hostName)
            try:
                # connect socket to port
                proxySocket.connect((hostName, serverPort))
                file = open(hostName, "w", encoding='utf=8')
                file.write(sentence.decode())
                proxySocket.send(sentence)
                proxySocket.settimeout(5)
                sentence = proxySocket.recv(4096)
                # create new file
                if (filename[-1:] == '/'):
                    filename = filename[:-1]
                newFile = open("./" + filename.replace("/",""), "wb")
                newFile.write(sentence)
                newFile.close()
                # send response
                connectionSocket.send(sentence)
            except Exception as e:
                print(e)
                print("Illegal request")
        else:
            pass
    connectionSocket.close()

