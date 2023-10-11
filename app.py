from flask import Flask, render_template, request
from myEphem import Ephem
import json
import random
from time import sleep
import datetime

from gpiozero import MCP3004
import RPi.GPIO as GPIO
import dht11

light_pins = [26, 19, 13, 6, 5]     # 5個の光センサーの状態を取得するラズパイのGPIOピン
humi_pin = 20
led_pin = 16
pilot_pin = 21
pilot_status = False
humi_sensor = dht11.DHT11(pin=humi_pin)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(pilot_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)
for pin in light_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


nagoya = {"place": "名古屋",
            "lat": 35.1667,
            "lon": 136.9167,
            "elev": 0}

battery = { "Ah": 100,
            "power": 12,    # LED消費電力（W）
            "cnt": 150,     # LED数
            "voltage": 24,  # 電圧（V）
            "BTcnt": 8,     # バッテリー個数
            "charge": 1500  # ソーラー＋風力での発電（Wh）
            }

# MCP3004でアナログ値を取得する
def analog_read(ch):
    adc = MCP3004(ch).value
    return adc

# 日時を文字列として返す
def getTime():
    dt = datetime.datetime.now()
    return dt.strftime("%Y/%m/%d %H:%M:%S")

# テキストに追記する
def addLog(text):
    with open("log.text", mode="a") as f:
        f.write(f"{getTime()}　{text}\n")

app = Flask(__name__)

@app.route("/")
def index():
    addLog("開始")
    return render_template("index.html")

@app.route("/getBattSetting", methods = ["POST"])
def getBattSetting():
    if request.method == "POST":
        return json.dumps(battery)             # 辞書をJSONにして返す


@app.route("/getEphem", methods = ["POST"])
def getEphem():
    try:
        ephem = Ephem(nagoya)       # 名古屋のEphemを取得する
        dict = ephem.get_data()     # データを辞書として取得する
    except Exception as e:
        message = str(e)
        dict = {"answer": message}  # エラーメッセージ
    addLog("暦算出")
    return json.dumps(dict)         # 辞書をJSONにして返す


# バッテリー電圧
@app.route("/getBatt", methods=["POST"])
def getBatt():
    if request.method == "POST":
        is_try = request.form["isTry"]
        dict = {}
        if is_try=="true":               # true/falseは文字列として送られてくる
            dict["ana3"] = random.randint(0, 100)
            dict["ana0"] = random.randint(0, 100)
            addLog(f"電圧（トライ）: {dict['ana3']}")
            print(f"電圧（トライ）:{dict}")
        else:
            ana3 = analog_read(ch=3)
            ana0 = analog_read(ch=0)
            dict["ana3"] = int(ana3*100)
            dict["ana0"] = int(ana0*100)
            addLog(f"電圧（本番）: {dict['ana3']}")
            print(f"電圧（本番）:{dict}")
        return json.dumps(dict)


# 温湿度計
@app.route("/getHumi", methods=["POST"])
def getHumi():
    if request.method == "POST":
        is_try = request.form["isTry"]
        dict = {}
        if is_try=="true":               # true/falseは文字列として送られてくる
            dict["temp"] = random.randint(10, 40)
            dict["humi"] = random.randint(0, 100)
            addLog(f"温度（トライ）: {dict['temp']}")
            addLog(f"湿度（トライ）: {dict['humi']}")
            print(f"温湿度（トライ）:{dict}")
        else:
            result = humi_sensor.read()
            if result.is_valid():
                dict["temp"] = round(result.temperature, 1) # 温度 小数第一位まで
                dict["humi"] = round(result.humidity, 1)    # 湿度 小数第一位まで
            else:
                dict["temp"] = "N/A"
                dict["humi"] = "N/A"
            addLog(f"温度（本番）: {dict['temp']}")
            addLog(f"湿度（本番）: {dict['humi']}")
            print(f"温湿度（本番）:{dict}")
        return json.dumps(dict)


# 光センサー
@app.route("/getLight", methods=["POST"])
def getLight():
    if request.method == "POST":
        is_try = request.form["isTry"]
        lights = []
        dict = {}
        if is_try=="true":               # true/falseは文字列として送られてくる
            for _ in light_pins:
                lights.append(random.choice([1, 0]))
            dict["lights"] = lights
            addLog(f"光センサー（トライ）: {dict['lights']}")
            print(f"光センサー（トライ）:{dict}")
        else:
            for pin in light_pins:
                lights.append(GPIO.input(pin))
            dict["lights"] = lights
            addLog(f"光センサー（本番）: {dict['lights']}")
            print(f"光センサー（本番）:{dict}")
        return json.dumps(dict)


# 育成LEDへの出力
@app.route("/enpowerLED", methods=["POST"])
def enpowerLED():
    if request.method == "POST":
        is_On = int(request.form["isOn"])
        if is_On:
            print("育成LEDオン")
            GPIO.output(led_pin, True)
        else:
            print("育成LEDオフ")
            GPIO.output(led_pin, False)
        return json.dumps({"response": "done"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(debug=True)
