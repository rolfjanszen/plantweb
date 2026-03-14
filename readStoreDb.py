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


def get_voltage(channel_nr):

    if is_raspberry_pi():
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        channel = AnalogIn(ads, channel_nr)

        # Read the voltage from the channel
        voltage = channel.voltage
        voltage = round(voltage,4)
    else:
        voltage = random.randint(0,100)
    return voltage


def read_and_store_ads1115(channel_nr):
   

    conn = sqlite3.connect('ads1115_readings.db')
    # Create single-ended input on channel 3 (A3)
    cursor = conn.cursor()

    # Get current Unix timestamp
    timestamp = int(time.time())
    voltage = get_voltage(channel_nr)
    # Connect to SQLite database (or create it if it doesn't exist)

    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS readings 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   timestamp INTEGER, 
                   voltage REAL, 
                   channel REAL)''')
    # Insert data
    print("channel vol",channel_nr,voltage,timestamp)
    cursor.execute('INSERT INTO readings (timestamp, voltage, channel) VALUES (?, ?, ?)', (timestamp, voltage, channel_nr))
    # Commit and close
    conn.commit()
    
    conn.close()
    #Wait for wrting to be done
    time.sleep(2)
    return timestamp, voltage

if __name__ =="__main__":

    while True:
        try:
            for i in range(3):
                t,v=read_and_store_ads1115(i)
            
                print(t,v)
        except Exception as e:
            print(e)
        time.sleep(1800)

# Example usage
timestamp, voltage = read_and_store_ads1115(0)
print(f"Stored reading: Timestamp = {timestamp}, Voltage = {voltage:.2f}")

