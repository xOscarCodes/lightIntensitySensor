import smbus
import time

# User "i2cdetect -y 1" to find device address from terminal
DEVICE = 0x23 

"""
Refrenced - https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiEzfSdibb7AhV-DrcAHSu2CnEQFnoECA4QAQ&url=https%3A%2F%2Fwww.mouser.com%2Fdatasheet%2F2%2F348%2Fbh1750fvi-e-186247.pdf&usg=AOvVaw3WnvnF5Wk7GBmdMu8AW8Tg
Page 5 - Instruction Set Architecture Table - Row 8 
1 lx precision. Measurement Time is typically 120ms.

Opecode for One Time High Res mode = 0010 0000
binary to hexa of Opecode is 20
"""
ONE_TIME_HIGH_RES_MODE_2 = 0x20

bus = smbus.SMBus(1) 

def convertToNumber(data):
    """ -- Summary -- 
        Function to convert value from the sensor to
        decimal
    Args:
        data (list): -- Description --
    data recieved from the light sensor
    data[0] = high byte
    data[1] = low byte 
    
    Conversion of high and low byte to low byte
    = high byte * 256 + low Byte
    
    Page - 2 Table - Electrical Characteristics - Row 4
    Typical measuurement accuracy of the sensor = 1.2 times
    So, (sensor out)/1.2
    
    Returns:
        float: decimal value 
    """
    return ((data[1] + (256 * data[0])) / 1.2)


def readLight(addr=DEVICE):
    """ -- Summary --
        Function to read sensor data
    Args:
        addr (hexa decimal, hexa decimal): _description_. Defaults to DEVICE which is 0x23.

    Returns:
        float: decimal value from sensor
    """
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_2)
    return convertToNumber(data)


def sensor():
    sensor_data = readLight()
    
    print("Illuminance: " + str(sensor_data) + " lux")
    
    if (sensor_data <= 25):
        print("Too Dark")
    elif (sensor_data > 25 and sensor_data <= 50):
        print("Dark")
    elif (sensor_data > 50 and sensor_data <= 75):
        print("Medium")
    elif (sensor_data > 75 and sensor_data <= 100):
        print("Bright")
    else:
        print("Too bright")
    
    time.sleep(1)


def main():    
    while True:
        sensor()


if __name__=="__main__":
    main()
