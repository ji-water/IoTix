import socket
import pymongo
from datetime import datetime, timedelta


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # str 인스턴스


# mongoDB connect
conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn.testDB_develop
collection = db.crop_part_schema
collection_crop = db.crop_schema
print("DB connection")

# socket open & listen
s = socket.socket()
s.bind(('0.0.0.0', 8080))
print("==socket open==")
s.listen(0)

# accept
while True:
    socketclient, addr = s.accept()

    # recv & DB upload
    while True:

        print("==========================")
        client_id = socketclient.recv(7)
        if len(client_id)==0:
            break
        print("crop_name : ", to_str(client_id)))
        client_part = socketclient.recv(5)
        print("crop_part_name : ", to_str(client_part))
        buff = socketclient.recv(1)
        #print(to_str(buff))
        length = socketclient.recv(int(buff))
        print("length : ", to_str(length))
        speed = socketclient.recv(12)
        print("speed : ", to_str(speed))
        now = datetime.now()
        print(now)

        if len(length) == 0 or to_str(speed) == "inf":
            break
        else:

            qs = collection_crop.find({"crop_name": to_str(client_id)})[0]  # crop_name_id
            # crop_id, crop_part_name --> 가장 lastest data length
            bqs = collection.find({"crop": qs['_id'], "crop_part_name": to_str(client_part)}).sort("date", -1).limit(1)[0]
            before_date = bqs["date"]
            before_len = bqs["length"]

            if ((now - before_date).days >= 1):
                days = (now - before_date).days
                print((now - before_date))
                date = before_date
                for i in range(days):
                    date = date + timedelta(days=1)
                    print(date)
                    temp_len = float(before_len)+float(speed)*86400
                    collection.insert_one(
                        {"crop": qs['_id'], "crop_part_name": to_str(client_part), "length": int(temp_len), "speed": float(speed), "date": date, "tag": 1})

            #print(addr[0])
            collection.insert_one({"crop": qs['_id'], "crop_part_name": to_str(client_part), "length": int(length), "speed": float(speed), "date": now, "tag": 0})
            print("========INSERT END========")

    print("Closing connection")
    socketclient.close()



