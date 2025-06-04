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

    # establish a baseline gas reading (Ω) for IAQ scoring
    baseline_gas = sensor.gas

    print("BME688 @ 0x77 – reading every 2 s (with IAQ)\n")
    while True:
        temp = sensor.temperature
        hum  = sensor.relative_humidity
        pres = sensor.pressure
        gas  = sensor.gas

        # --- simple IAQ calculation ---
        # humidity_score: best at 40% RH, linear drop‐off
        humidity_score = max(0, 100 - 5 * abs(hum - 40))
        # gas_score: relative to baseline, capped 0–100
        gas_score = min(max((gas / baseline_gas) * 100, 0), 100)
        # weighted sum (25% humidity, 75% gas)
        iaq = humidity_score * 0.25 + gas_score * 0.75
        # --------------------------------

        print(f"Temp:     {temp:.2f} °C")
        print(f"Humidity: {hum:.2f} %")
        print(f"Pressure: {pres:.2f} hPa")
        print(f"Gas:      {gas:.0f} Ω")
        print(f"IAQ:      {iaq:.2f}  (0=poor → 100=excellent)")
        print("-" * 30)

        time.sleep(2)

if __name__ == "__main__":
    main()