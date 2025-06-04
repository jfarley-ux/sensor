# SCD40 + BME688 Environmental Sensors for Raspberry Pi

This project reads environmental data from two sensors:
- **SCD40**: CO2, temperature, and humidity via I2C
- **BME688**: Temperature, humidity, pressure, gas resistance, and altitude via I2C

## Hardware Requirements

- Raspberry Pi Zero 2 W
- Sensirion SCD40 CO2 sensor
- Bosch BME688 environmental sensor

## Wiring

### SCD40 (I2C):
- SCD40 VDD → Pi 3.3V (Pin 1)
- SCD40 GND → Pi GND (Pin 6)
- SCD40 SDA → Pi GPIO 2 (Pin 3)
- SCD40 SCL → Pi GPIO 3 (Pin 5)
- SCD40 I2C address may be 0x44 or default 0x62 (scan with `i2cdetect`)

### BME688 (I2C - Custom Pins):
- BME688 VCC → Pi 5V (Pin 2)
- BME688 GND → Pi GND (Pin 9)
- BME688 SDA → Pi GPIO 17 (Pin 11)
- BME688 SCL → Pi GPIO 27 (Pin 13)

## Installation

1. Enable I2C:
   ```bash
   sudo raspi-config
   ```
   Interface Options > I2C > Enable

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python3 scd40_sensor.py
   ```

## Sensor Data

**SCD40 provides:**
- CO2 concentration (ppm)
- Temperature (°C)
- Relative humidity (%)

**BME688 provides:**
- Temperature (°C)
- Relative humidity (%)
- Atmospheric pressure (hPa)
- Gas resistance (Ohms) - for air quality estimation
- Calculated altitude (m)

## Git Usage

After making changes, run:

```bash
cd "c:\Users\jamie\Desktop\Sites\HTML and Python\environment"
git add .
git commit -m "Describe your changes"
git push origin main
```

If this is your first push or you renamed branches:

```bash
git branch -M main
git push -u origin main
```
