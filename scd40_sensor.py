import time
import board
import busio
import adafruit_bme680

def main():
    # set up I²C and BME688 @ 0x77
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x77)

    # adjust to your local sea-level pressure
    sensor.sea_level_pressure = 1013.25

    print("BME688 @ 0x77 – reading every 2 s\n")
    while True:
        print(f"Temp:     {sensor.temperature:.2f} °C")
        print(f"Humidity: {sensor.relative_humidity:.2f} %")
        print(f"Pressure: {sensor.pressure:.2f} hPa")
        print(f"Gas:      {sensor.gas:.0f} Ω")
        print("-" * 30)
        time.sleep(2)

if __name__ == "__main__":
    main()