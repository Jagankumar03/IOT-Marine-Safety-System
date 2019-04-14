import serial
import time

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)
data = '0'
while True:
    #data='\0'
    #rcv='\0'
    #port.write("\r\nSay something:")
    rcv = port.read(1)
    if (rcv == '$'):
        print('1')
        rcv = port.read(1)
        if (rcv == 'G'):
            print('2')
            rcv = port.read(1)
            if (rcv == 'P'):
                print('3')
                rcv = port.read(1)
                if (rcv == 'G'):
                    print('4')
                    rcv = port.read(1)
                    if (rcv == 'G'):
                        print('5')
                        rcv = port.read(1)
                        if (rcv == 'A'):
                            print('6')
                            while(rcv != '$'):                                
                                data += rcv
                                rcv = port.read(1)
                        print('************data received*****************')
                        time.sleep(2)
                        print(data)
                        f=open('gps_data.txt','w')
                        f.write('https://www.google.co.in/maps/@'+data)
                        f.close()
                        time.sleep(2)
                        data=''
                        rcv=''
                        

    #port.write("\r\nYou sent:" + repr(rcv))

