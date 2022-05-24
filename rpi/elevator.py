import time, random, requests
import DAN
from concurrent.futures import ThreadPoolExecutor

import RPi.GPIO as GPIO

segmentLatch = 20
segmentClock = 21
segmentData = 16
left = 23
right = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(segmentClock, GPIO.OUT)
GPIO.setup(segmentLatch, GPIO.OUT)
GPIO.setup(segmentData, GPIO.OUT)
GPIO.setup(left, GPIO.OUT)
GPIO.setup(right, GPIO.OUT)

GPIO.output(segmentClock, GPIO.LOW)
GPIO.output(segmentLatch, GPIO.LOW)
GPIO.output(segmentData, GPIO.LOW)


def postNumber(number):
    if number == 1:
        segments = "11110011"
    elif number == 2:
        segments = "01001001"
    elif number == 3:
        segments = "01100001"
    elif number == 4:
        segments = "00110011"
    elif number == 5:
        segments = "00100101"
    elif number == 6:
        segments = "00000111"
    elif number == 7:
        segments = "10110001"
    elif number == 8:
        segments = "00000000"
    elif number == 9:
        segments = "00110001"
    elif number == 0:
        segments = "10000001"


    GPIO.output(segmentLatch, GPIO.LOW)
    for n in range(8):
        GPIO.output(segmentData, int(segments[n]))
        GPIO.output(segmentClock, GPIO.HIGH)
        GPIO.output(segmentClock, GPIO.LOW)
    GPIO.output(segmentLatch, GPIO.HIGH)

def showNum(i):
    for u in range(50):
        GPIO.output(left, GPIO.LOW)
        GPIO.output(right, GPIO.HIGH)
        postNumber(i//10)
        time.sleep(.01)
        GPIO.output(left, GPIO.HIGH)
        GPIO.output(right, GPIO.LOW)
        postNumber(i%10)
        time.sleep(.01)



#ServerURL = 'http://IP:9999'      #with non-secure connection
ServerURL = 'https://demo.iottalk.tw' #with SSL connection # 可改名稱
Reg_addr = '236MAC1' #if None, Reg_addr = MAC address # 可改名稱

DAN.profile['dm_name']='Dummy_Device'
DAN.profile['df_list']=['Dummy_Sensor', 'Dummy_Control',]
DAN.profile['d_name']= '23601' # 可改名稱

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line


def write_data():
    while True:
        try:
            #IDF_data = random.uniform(1, 10)
            #DAN.push ('Dummy_Sensor', IDF_data) #Push data to an input device feature "Dummy_Sensor"

            #==================================

            ODF_data = DAN.pull('Dummy_Control')#Pull data from an output device feature "Dummy_Control"
            if ODF_data != None:
                print (ODF_data[0])
                showNum(int(ODF_data[0]))

        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)    

        time.sleep(0.2)


with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(write_data)
