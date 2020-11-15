import netmiko
import getpass

#Get switch IP
ip = input("Enter device IP/FQDN: ")

#Get the username and password
username = input("user: ")
passwd = getpass.getpass("pass: ")

try:
    #Connect to the switch
    device = netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=passwd)

    #Write message stating successful connection
    print("Connected successfully to " + ip )

    #Get show interfaces output
    showintoutput = device.send_command("show interfaces")

    #Disconnect from the switch
    device.disconnect()

    interfaceline = ""
    lastusedline = ""
    finaloutput = ""
    numfreeports = 0

    #For each line in the command output
    for line in showintoutput.splitlines():
        if "protocol" in line:
            interfaceline = line
        if "Last input" in line:
            lastusedline = line
            if ('y' in lastusedline or ("input never" in lastusedline and "output never" in lastusedline)) and not (':' in lastusedline):
                finaloutput += interfaceline + "\n" + lastusedline + "\n"
                numfreeports += 1

    print("\nPorts not used in over a year:  " + str(numfreeports) + "\n\n")
    print(finaloutput)

except:
    print("Could not connect to the device")
