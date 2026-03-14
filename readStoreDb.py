import sqlite3
import time
import random


def is_raspberry_pi():
    try:
        # Check if the hardware description file exists (Pi specific)
        if os.path.exists('/proc/device-tree/model'):
            with open('/proc/device-tree/model', 'r') as f:
                return 'Raspberry Pi' in f.read()
    except Exception:
        return False
    return False

if is_raspberry_pi():
    import board
    import busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn


    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the ADC object using the I2C bus
    ads = ADS.ADS1115(i2c)

    conn = sqlite3.connect('ads1115_readings.db')
    soil_channels =[AnalogIn(ads, 0), AnalogIn(ads, 1), AnalogIn(ads, 2)]
else:
    soil_channels = [None, None, None]


def get_average_voltage(channel):

    volt_sum = 0
    volt_count = 0
    for i in range(4):
        voltage = channel.voltage
        volt_sum += voltage
        volt_count += 1
        time.sleep(0.5)
    return volt_sum/volt_count


def read_sinle_channel(channel_nr):   

    conn = sqlite3.connect('ads1115_readings.db')
    # Create single-ended input on channel 3 (A3)
    cursor = conn.cursor()
    if is_raspberry_pi():
    # Read the voltage from the channel
        voltage = get_average_voltage(soil_channels[channel_nr])
    else:
        voltage = random.randint(0,3)
    
    timestamp = int(time.time())
    # Insert data
    print("channel vol",channel_nr,voltage,timestamp)
    time.sleep(1)
    cursor.execute('INSERT INTO readings (timestamp, voltage, channel) VALUES (?, ?, ?)', (timestamp, voltage, channel_nr))
    
    # Commit and close
    conn.commit()
    conn.close()
    #Wait for wrting to be done
    time.sleep(2)
    return timestamp, voltage


def read_and_store_ads1115():
    
    
    conn = sqlite3.connect('ads1115_readings.db')
    # Create single-ended input on channel 3 (A3)
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS readings 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   timestamp INTEGER, 
                   voltage REAL, 
                   channel REAL)''')
    for channel_nr,channel in enumerate(soil_channels):

        if is_raspberry_pi():
        # Read the voltage from the channel
            voltage = get_average_voltage(channel)
        else:
            voltage = random.randint(0,3)
    
        timestamp = int(time.time())
        # Insert data
        print("channel vol",channel_nr,voltage,timestamp)
        time.sleep(1)
        cursor.execute('INSERT INTO readings (timestamp, voltage, channel) VALUES (?, ?, ?)', (timestamp, voltage, channel_nr))
        
    # Commit and close

    conn.commit()
    
    conn.close()
    #Wait for wrting to be done
    time.sleep(2)
    return timestamp, voltage

if __name__ =="__main__":

    while True:

        t,v=read_and_store_ads1115()
        print(t,v)
        
        time.sleep(5)


