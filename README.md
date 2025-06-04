# SCD40 CO2 Sensor for Raspberry Pi

This project reads CO2, temperature, and humidity data from a Sensirion SCD40 sensor using a Raspberry Pi Zero 2 W.

## Hardware Requirements

- Raspberry Pi Zero 2 W
- Sensirion SCD40 CO2 sensor
- I2C connection (SDA to GPIO 2, SCL to GPIO 3)

## Installation

1. Enable I2C on your Pi:
   ```bash
   sudo raspi-config
   ```
   Navigate to Interface Options > I2C > Enable

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python3 scd40_sensor.py
   ```

## Wiring

- SCD40 VDD → Pi 3.3V
- SCD40 GND → Pi GND  
- SCD40 SDA → Pi GPIO 2 (SDA)
- SCD40 SCL → Pi GPIO 3 (SCL)

## Usage

The script will continuously read and display sensor data every 5 seconds. Press Ctrl+C to stop.
