import serial
import time

ser = serial.Serial('COM4', 9600, timeout=1)

ser.write(b'<>')
time.sleep(1)

#commands
# <power, ignitor charge, cap charge, cap charge rate, trigger, ignite bleed, cap bleed>

def processCommand(CMD,MSG):
    encodedCMD = bytes(CMD,'utf-8')
    ser.write(encodedCMD)
    #now wait to recieve reply
    print(MSG)
    controlStatus()
        
def controlStatus():
    while True:
        response = ser.readline()
        # confirm Arduino executed
        if b'OK' in response:
            print('command complete')
            break

def testIgnitronAndBleed():
    # power on
    command = "<1>"
    processCommand(command)
    print("Power on")
    time.sleep(1)
    
    # disconnect ingitron bank bleed resistor
    command = '<1,0,0,0,0,1>'
    processCommand(command)
    time.sleep(1)
    
    # charge ignitron bank
    command = '<1,1,0,0,0,1>'  # Ensure your command matches the expected format
    processCommand(command)
    time.sleep(15)
    
    # stop charging ignitron bank
    command = '<1,0,0,0,0,1>'
    processCommand(command)
    time.sleep(1)
    
    # bleed ignitron bank
    command = '<1,0,0,0,0,0>'
    processCommand(command)
    time.sleep(10)
    
    # turn off power
    command = '<0,0,0,0,0,0,0,0>'
    processCommand(command)
    
    print("test complete")
    
def testConditionAndBleed():
    # power on
    command = "<1>"
    processCommand(command,'PWR')
    
    # disconnect cap bank bleed resistor
    command = "<1,0,0,0,0,0,1>"
    processCommand(command,'BLD_OFF')
    
    # slow charge cap bank
    command = "<1,0,1,0,0,0,1>"
    processCommand(command,'CHRG')
    
    # stop charging cap bank
    command = "<1,0,0,0,0,0,1>"
    processCommand(command,'CHRG_STOP')
    
    # bleed cap bank
    command = "<1,0,0,0,0,0,0>"
    processCommand(command,'BLD')
    
    print("test complete")
    
def testFastAndBleed():
    # power on
    command = "<1>"
    processCommand(command,'PWR_ON')
    print("Power on")
    
    # disconnect cap bank bleed resistor
    command = "<1,0,0,0,0,0,1>"
    processCommand(command,'BLD_OFF')
    
    # fast charge cap bank
    command = "<1,0,1,1,0,0,1>"
    processCommand(command,'CHRG')
    
    # stop charging cap bank
    command = "<1,0,0,0,0,0,1>"
    processCommand(command,'STOP')
    
    # bleed cap bank
    command = "<1,0,0,0,0,0,0>"
    processCommand(command,'BLD')

    print("test complete")
    
def fastCharge():
    # power on
    command = "<1>"
    processCommand(command,'PRW_ON')
    print("Power on")
    
    # disconnect cap bank bleed resistor
    command = "<1,0,0,0,0,0,1>"
    processCommand(command,'BLD_OFF')
    
    # fast charge cap bank
    command = "<1,0,1,1,0,0,1>"
    processCommand(command,'CHRG')
    
    # stop charging cap bank
    command = "<1,0,0,0,0,0,1>"
    processCommand(command,'STOP')
    
def ignitronCharge(t):
    # power on
    command = "<1>"
    processCommand(command,'PWR')
    print("Power on")
    time.sleep(1)
    
    # disconnect ingitron bank bleed resistor
    command = '<1,0,0,0,0,1>'
    processCommand(command,'BLD_OFF')
    time.sleep(1)
    
    # charge ignitron bank
    command = '<1,1,0,0,0,1>'  # Ensure your command matches the expected format
    processCommand(command, 'CHRG')
    time.sleep(t)
    
    # stop charging ignitron bank
    command = '<1,0,0,0,0,1>'
    processCommand(command,'STOP_CHRG')
    time.sleep(0.1)
    
    
def discharge(t):   
    # power on
    command = "<1>"
    processCommand(command,'PWR')
    print("Power on")
    time.sleep(1)

    # disconnect ingitron bank bleed resistor
    command = '<1,0,0,0,0,1>'
    processCommand(command,'BLD_OFF')
    time.sleep(1)
    
    # charge ignitron bank
    command = '<1,1,0,0,0,1>'  # Ensure your command matches the expected format
    processCommand(command,'CHRG')
    time.sleep(t)

    
    # trigger ignitron
    command = '<1,0,0,0,1,1>'
    processCommand(command,'TGR')
    
    # close trigger relay and bleed remaining charge
    command = '<1,0,0,0,0,0,0>'
    processCommand(command,'BLD')
    
def powerOff():
    # turn off power
    command = '<0,0,0,0,0,0,0,0>'
    processCommand(command,'PWR_OFF')
    
def powerOn():
    # power on
    command = "<1>"
    processCommand(command,'PWR_ON')
    print("Power on")

#powerOn()

testConditionAndBleed()

#testFastAndBleed()

#fastCharge()

#discharge(5)

powerOff()

ser.close()
