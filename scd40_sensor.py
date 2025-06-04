#!/usr/bin/env python3
"""
SCD40 CO2 + BME688 Environmental Sensor Reader for Raspberry Pi Zero 2 W
Reads CO2, temperature, and humidity from SCD40 sensor (I2C)
Reads temperature, humidity, pressure, and gas resistance from BME688 sensor (I2C)
"""

import os
# Force Blinka to use pigpio as its GPIO/I2C driver
os.environ["BLINKA_FORCE_PIGPIO"] = "1"

import time
import pigpio
import board
import busio
import digitalio
from adafruit_scd4x import SCD4X
import adafruit_bme680

def main():
    # Initialize pigpio daemon interface (no further use but required)
    pi = pigpio.pi()
    if not pi.connected:
        print("Failed to connect to pigpio daemon; ensure `sudo pigpiod` is running")
        return

    try:
        # Initialize I2C bus for SCD40 on standard pins
        # SCD40 connections:
        # SCD40 VDD → Pi 3.3V (Pin 1)
        # SCD40 GND → Pi GND (Pin 6)
        # SCD40 SDA → Pi GPIO 2 (Pin 3) - I2C Data
        # SCD40 SCL → Pi GPIO 3 (Pin 5) - I2C Clock
        
        # BME688 connections on custom pins:
        # BME688 VCC → Pi 3.3V (Pin 2)
        # BME688 GND → Pi GND (Pin 9)
        # BME688 SDA → Pi GPIO 17 (Pin 11) - Custom I2C Data
        # BME688 SCL → Pi GPIO 27 (Pin 13) - Custom I2C Clock
        
        # Standard I2C for SCD40
        i2c = busio.I2C(board.SCL, board.SDA)  # GPIO 3 = SCL, GPIO 2 = SDA
        
        # Scan for I2C devices to debug
        print("Scanning I2C bus for devices...")
        while not i2c.try_lock():
            pass
        try:
            devices = i2c.scan()
            print(f"I2C devices found: {[hex(device) for device in devices]}")
        finally:
            i2c.unlock()
        
        # Choose SCD40 address based on scan (0x44 if present, else default 0x62)
        addr = 0x44 if 0x44 in devices else 0x62
        try:
            scd4x = SCD4X(i2c, address=addr)
            print(f"SCD40 initialized at 0x{addr:02X}")
        except Exception as e:
            print(f"SCD40 initialization failed at 0x{addr:02X}: {e}")
            print("Check wiring and ensure correct SDA/SCL pins")
            return
        
        # Custom I2C for BME688 on pins 11 and 13
        i2c_custom = busio.I2C(board.D27, board.D17)  # SCL=GPIO27 (Pin 13), SDA=GPIO17 (Pin 11)
        
        # Scan custom I2C bus
        print("Scanning custom I2C bus for BME688...")
        while not i2c_custom.try_lock():
            pass
        try:
            devices_custom = i2c_custom.scan()
            print(f"Custom I2C devices found: {[hex(device) for device in devices_custom]}")
        finally:
            i2c_custom.unlock()
        
        bme688 = None
        try:
            # Try BME688 at different possible addresses
            if 0x77 in devices_custom:
                bme688 = adafruit_bme680.Adafruit_BME680_I2C(i2c_custom, address=0x77)
                print("BME688 initialized successfully at address 0x77")
            elif 0x76 in devices_custom:
                bme688 = adafruit_bme680.Adafruit_BME680_I2C(i2c_custom, address=0x76)
                print("BME688 initialized successfully at address 0x76")
            else:
                bme688 = adafruit_bme680.Adafruit_BME680_I2C(i2c_custom)
                print("BME688 initialized successfully")
        except Exception as e:
            print(f"BME688 initialization failed: {e}")
            print("Continuing with SCD40 only...")
            print("Check BME688 wiring:")
            print("  VCC → Pin 2 (5V)")
            print("  GND → Pin 9 (GND)")
            print("  SDA → Pin 11 (GPIO 17)")
            print("  SCL → Pin 13 (GPIO 27)")
        
        print("Sensor initialization complete...")
        
        # Configure BME688 if available
        if bme688:
            bme688.sea_level_pressure = 1013.25  # Sea level pressure in hPa
        
        # Start periodic measurement for SCD40
        scd4x.start_periodic_measurement()
        print("Sensors started. Waiting for measurements...")
        
        # Wait for first measurement
        time.sleep(5)
        
        while True:
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Read SCD40 data
            if scd4x.data_ready:
                co2 = scd4x.CO2
                scd40_temp = scd4x.temperature
                scd40_humidity = scd4x.relative_humidity
                
                print("SCD40 Readings:")
                print(f"  CO2: {co2} ppm")
                print(f"  Temperature: {scd40_temp:.1f} °C")
                print(f"  Humidity: {scd40_humidity:.1f} %")
            else:
                print("SCD40: Data not ready")
            
            # Read BME688 data only if sensor is available
            if bme688:
                try:
                    bme688_temp = bme688.temperature
                    bme688_humidity = bme688.relative_humidity
                    pressure = bme688.pressure
                    gas_resistance = bme688.gas
                    altitude = bme688.altitude
                    
                    print("BME688 Readings:")
                    print(f"  Temperature: {bme688_temp:.1f} °C")
                    print(f"  Humidity: {bme688_humidity:.1f} %")
                    print(f"  Pressure: {pressure:.2f} hPa")
                    print(f"  Gas Resistance: {gas_resistance:.0f} Ohms")
                    print(f"  Altitude: {altitude:.1f} m")
                except Exception as e:
                    print(f"BME688 Error: {e}")
            else:
                print("BME688: Not available")
            
            print("-" * 50)
            
            # Wait 10 seconds between readings
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\nStopping sensor readings...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            scd4x.stop_periodic_measurement()
            print("Sensors stopped.")
        except:
            pass

if __name__ == "__main__":
    main()
