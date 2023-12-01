from configuration_manager import ConfigurationManager
from multi_uart_controller import MultiUARTController
import serial_assistance as sa
import time
import calc

if __name__ == "__main__":
    
    config_man = ConfigurationManager("configuration/")
    config = config_man.read_config_file()

    selected_port = sa.get_port_by_name(config.get('port_by_name'))
    if(selected_port):
        mc_control = MultiUARTController(selected_port)
        mc_control.set_power_to_all_channels(state = 0)
        
        with open(f"{config.get('data_directory')}{config.get('desiccation_filename')}", 'a') as f:
                f.write(f'"epoch{time.time()}":{{\n')
                
        #while(1):
        for device in range(config.get('num_devices')):
            
            mc_control.set_power_to_channel(channel = device,state = 1)
            time.sleep(0)
            mc_control.set_communication_channel(channel = device,baud = 0)
            
            #PREAMBLE CHECK
            preamble = []
            preamble_fail = False
            n = 0
            # Added this while loop to signifincantly speed up the checking for connections, not very safe though
            # THe system does seem reliable enough though
            while( n < 5):
                data = mc_control.read_byte()
                preamble.append(data)
                n+=1
                if(data != 85):
                    preamble_fail = True
                    print(f'Connection Timed Out for Device {device}')
                    message = f'"D{device}": {{" Temp":0, "Moisture":0, "Bad Data":"NO DEVICE FOUND"}}'
                    break

            if (preamble_fail==False): # If preamble was right
                print(f"Connected to Device {device}")
                data = []
                #Start adding data to list
                if (preamble_fail==False): # If preamble was right
                    for packet in range(config.get('bytes_received') - 5):
                        data.append(mc_control.read_byte())
                
                # this relates specifically to the temp spike data laypout
                # First check post-amble for correct thing
                corrupt = False 
                correct_postamble = [170, 171, 186, 172, 202]
                for n in range(len(correct_postamble)):
                    if(data[len(data)-5+n] != correct_postamble[n]):
                        corrupt = True
                # Time for correct data layout
                
                #TEMP CALCULATION
                message = f'"D{device}": {{ "Temp": ['
                temp = []
                i = 0
                for i in range(5):
                    temp.append(data[i+1]*256+data[i])
                    i+=2
                
                i = 0
                temp = calc.toTemp(temp)
                for i in range(len(temp)-1):
                    message += str(temp[i]) + ','
                i+=1
                message += str(temp[i])
                
                message += '], "Resistances": ['
                
                # MOIST CALCULATION
                moist = []
                i=0
                while(i<len(data)-16):
                    moist.append(data[i+11]*256+data[i+10])
                    i+=2
                
                resistances = calc.toResistance(moist)
                i=0
                for i in range(len(resistances)-1):
                    message+= str(resistances[i] ) +', '
                i+=1
                message += str(resistances[i])
                message += f'], "Bad Data": "{corrupt}"}}'
            
            mc_control.set_power_to_channel(channel = device,state = 0)
            with open(f"{config.get('data_directory')}{config.get('desiccation_filename')}", 'a') as f:
                if (device == config.get('num_devices')-1):
                    f.write(f' {message}}},\n')
                else:
                    f.write(f' {message},\n')
            
            print(f"Data saved in {config.get('desiccation_filename')}")
    else:
        print("No device found, confirm configuration settings and pip")