import serial.tools.list_ports # type: ignore


def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = splitPort[0]
    # return commPort
    return "COM1"


if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    print(ser)


def processData(client, data):
    print("data wite:",data)
    
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    if splitData[0] == "T":
        client.publishMessage("theloc3101/feeds/temperature_history", splitData[1])
    elif splitData[0] == "H":
        client.publishMessage("theloc3101/feeds/humid_history", splitData[1])
    elif splitData[0] == "L":
        client.publishMessage("theloc3101/feeds/light_history", splitData[1])


mess = ""


def readSerial(client):
    bytesToRead = ser.inWaiting()
    # print("bytesToRead: ",bytesToRead)
    
    if bytesToRead > 0:
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        print("read: ",mess)
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start : end + 1])
            if end == len(mess):
                mess = ""
            else:
               mess = mess[end + 1 :]
    else:
        return



def writeSerial(data):
    ser.write(str(data).encode())
