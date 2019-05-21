import socket
import pymongo
import datetime

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value # str 인스턴스

#mongoDB connect
conn = pymongo.MongoClient('127.0.0.1',27017)
db = conn.IOTIX
collection = db.IOTIX_data

#socket open & listen
s = socket.socket()
s.bind(('0.0.0.0',8090))
s.listen(0)

#accept 
while True:
    socketclient,addr = s.accept()

    #recv & DB upload
    while True:
        client_id= socketclient.recv(32)
        time = socketclient.recv(25)
        content = socketclient.recv(16)
        print(to_str(content));
       

        if len(content)==0:
            break
        else:
            print(addr[0])
            print(content)
            collection.insert({to_str(client_id):to_str(content),"time":to_str(time)})
            #find
            docs=collection.find()
            for i in docs:
                print (i)
                
    print("Closing connection")
    socketclient.close()



