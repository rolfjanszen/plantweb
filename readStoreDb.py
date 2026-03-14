import sqlite3
import time
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


def read_and_store_ads1115():
    
    
    conn = sqlite3.connect('ads1115_readings.db')
    # Create single-ended input on channel 3 (A3)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS readings (timestamp INTEGER PRIMARY KEY, voltage REAL, channel REAL)''')
    for channel_nr,channel in enumerate(soil_channels):
        # Read the voltage from the channel
        voltage = channel.voltage
        voltage = round(voltage,4)
        # Get current Unix timestamp
        timestamp = int(time.time())

        cursor.execute('''CREATE TABLE IF NOT EXISTS readings (timestamp INTEGER PRIMARY KEY, voltage REAL, channel REAL)''')

        # Insert data
        print("channel vol",channel_nr,voltage,timestamp)
        cursor.execute('INSERT INTO readings (timestamp, voltage, channel) VALUES (?, ?, ?)', (timestamp, voltage, channel_nr))
        time.sleep(1)
        # Commit and close
    conn.commit()
    
    conn.close()
    #Wait for wrting to be done
    time.sleep(1)
    return timestamp, voltage

if __name__ =="__main__":

    while True:
        try:
            t,v=read_and_store_ads1115()
            print(t,v)
        except Exception as e:
            print(e)
        time.sleep(2)

# Example usage
timestamp, voltage = read_and_store_ads1115()
print(f"Stored reading: Timestamp = {timestamp}, Voltage = {voltage:.2f}")

