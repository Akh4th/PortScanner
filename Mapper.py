from socket import *
import socket as socket1
import time
from termcolor import colored as c
import ipaddress


# Global Settings
global record
res = {}
# Determine weather to create a log file or not
record = input("Would you like to record the scanning ?" + c("\n[Yes/No] : ", "red"))
if record.upper() == "YES" or record == 1:
    record = True
else:
    record = False


# Creating a header to the log file
def rec():
    file = open('NetMap.txt', 'a')
    file.write(f"Scanning started at : {tim}\nScanning the target {ip} in range of {portA}-{portB}\n")
    file.close()


# Writing every open port in the log file
def rec2(number, name):
    file = open('NetMap.txt', 'a')
    file.write(f"{name} active on port {number} !")
    file.close()


# Determine service version
def ver(host, ser):
    try:
        s = socket1.socket()
        s.connect((host, ser))
        if ser == 80:
            x = "GET / HTTP/1.0\r\n\r\n"
            s.send(x.encode())
            print(c(f"http://{ip}/", "blue") + " - " + s.recv(1024).decode().split("\n")[1])
        elif ser == 443:
            print(c(f"https://{ip}/", "blue"))
        else:
            print(s.recv(1024).decode())
    except Exception as e:
        print(c("ERROR WHILE CHECKING VERSION. ", "red") + c(f"ERROR CODE : {e}", "yellow"))


def scan(a, b, IP):
    for i in range(a, b + 1):
        amount = b - a + 1
        per = (int(i) * 100) / int(amount)
        long = time.time() - tim
        soc = socket(AF_INET, SOCK_STREAM)
        con = soc.connect_ex((IP, i))
        if con == 0:
            res[i] = socket1.getservbyport(i, "tcp")
            if record:
                rec2(i, socket1.getservbyport(i, "tcp"))
        print("\r" + c(str(i) + "/" + str(amount), "green") + "\t\t" + c(str(round(per, 2)) + "%\t\t", "blue") + c(str(format(round(long, 2)) + "s\t\t", ), "yellow"), end=" ")
    soc.close()
    ends()


def ends():
    print(c("\n\nSCAN IS OVER, ", "red") + c(len(res), "yellow") + c(" PORTS WERE FOUND !\n", "red"))
    time.sleep(2)
    res1 = res.items()
    for item in res1:
        port, serv = item
        print("The service " + c(serv, "red") + " is active, port : " + c(port, "red"))
        ver(ip, port)


try:
    ip = input("\nEnter the " + c("IP Address", "red") + " you'd like to scan : ")
    # Getting only legit values
    try:
        print("\nPlease enter ports range")
        portA = int(input(c("Starts with : ", "blue")))
        portB = int(input(c("Ends with : ", "yellow")))
        while portA < 0:
            portA = input(c("Port number has to be positive number.", "green"))
        while portB < 0:
            portB = input(c("Port number has to be positive number.", "green"))
    except ValueError:
        print(c("Port has to be a number !", "red"))
        quit()
    # Validating IP Address for scanning
    try:
        tim = time.time()
        # Begins the scan only when given input is a valid IP Address
        if ipaddress.ip_address(ip):
            if record:
                rec()
            print("\nScanning the target " + c(ip, "red") + " in range of " + c(str(portA) + "-" + str(portB) + "\n", "blue"))
            print(c("PORTS\t\t", "green") + c("PROCESS\t\t", "blue") + c("DURATION\t\t", "yellow"))
            scan(portA, portB, ip)
    except ValueError:
        print(c("The IP Address is not responding.\nPlease try again.\n", "red"))
except KeyboardInterrupt:
    print("Keyboard interrupt detected !\nABORTING !!!")
    quit()

