#!/usr/bin/env python3
"""
SCD40 CO2 Sensor Reader for Raspberry Pi Zero 2 W
Reads CO2, temperature, and humidity from Sensirion SCD40 sensor
"""

import time
import board
import busio
from adafruit_scd4x import SCD4X

def main():
    try:
        # Initialize I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        scd4x = SCD4X(i2c)
        
        print("SCD40 CO2 Sensor Initializing...")
        
        # Start periodic measurement
        scd4x.start_periodic_measurement()
        print("Sensor started. Waiting for measurements...")
        
        # Wait for first measurement (SCD40 needs ~5 seconds)
        time.sleep(5)
        
        while True:
            if scd4x.data_ready:
                # Read sensor data
                co2 = scd4x.CO2
                temperature = scd4x.temperature
                humidity = scd4x.relative_humidity
                
                # Display readings
                print(f"CO2: {co2} ppm")
                print(f"Temperature: {temperature:.1f} °C")
                print(f"Humidity: {humidity:.1f} %")
                print("-" * 30)
            
            # Wait 5 seconds between readings
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nStopping sensor readings...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            scd4x.stop_periodic_measurement()
            print("Sensor stopped.")
        except:
            pass

if __name__ == "__main__":
    main()
