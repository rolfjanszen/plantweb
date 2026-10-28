import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus (automatically uses GPIO 3 for SCL and GPIO 2 for SDA)
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADS1115 ADC object
ads = ADS.ADS1115(i2c)

# Optionally, adjust the gain (default is 1, which measures up to +/-4.096V)
# ads.gain = 1

# Create a single-ended input on channel 0 (connect your sensor's output here)
chan = AnalogIn(ads, 0)

print("Reading ADS1115 Channel 0... Press Ctrl+C to stop.\n")

try:
    while True:
        print(f"Raw Value: {chan.value} \t Voltage: {chan.voltage:.3f}V")
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nExiting program.")
