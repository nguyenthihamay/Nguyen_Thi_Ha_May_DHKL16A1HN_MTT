
import paho.mqtt.client as mqtt 
import csv 
import time 
import json 
import matplotlib.pyplot as plt 
 
CSV_FILE = "sensor_data.csv" 
MQTT_BROKER = "broker.hivemq.com" 
MQTT_PORT = 1883 
MQTT_TOPIC = "iot/khdl/esp32" 
 
# Tạo file CSV nếu chưa có 
with open(CSV_FILE, mode='w', newline='') as file: 
    writer = csv.writer(file) 
    writer.writerow(["timestamp", "temperature", "humidity"]) 
 
temps, hums, times = [], [], [] 
 
def on_connect(client, userdata, flags, rc): 
    if rc == 0: 
        print(" Đã kết nối MQTT broker.") 
        client.subscribe(MQTT_TOPIC) 
    else: 
        print(" Kết nối thất bại, mã lỗi:", rc) 
 
def on_message(client, userdata, msg): 
    try: 
        data = json.loads(msg.payload.decode()) 
        timestamp = data.get("timestamp", time.time()) 
        temp = data.get("temperature", 0) 
        hum = data.get("humidity", 0) 
 
        print(f" Dữ liệu nhận được: {timestamp}, {temp}, {hum}") 
 
        with open(CSV_FILE, mode='a', newline='') as file: 
            writer = csv.writer(file) 
            writer.writerow([timestamp, temp, hum]) 
 
        temps.append(temp) 
        hums.append(hum) 
        times.append(timestamp) 
 
        # Vẽ biểu đồ sau mỗi 10 bản ghi 
        if len(temps) % 10 == 0: 
            plt.clf() 
            plt.subplot(2,1,1) 
            plt.plot(times, temps, 'r-', label='Nhiệt độ (°C)') 
            plt.legend() 
            plt.subplot(2,1,2) 
            plt.plot(times, hums, 'b-', label='Độ ẩm (%)') 
            plt.legend() 
            plt.pause(0.1) 
 
    except Exception as e: 
        print(" Lỗi xử lý dữ liệu:", e) 
 
client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message 
 
client.connect(MQTT_BROKER, MQTT_PORT, 60) 
plt.ion()  # Bật chế độ vẽ tương tác 
client.loop_forever() 