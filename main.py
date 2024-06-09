from modbus485 import*
from mqtt import*
import time
import serial as serial

try:
    ser = serial.Serial(port="/dev/ttyUSB0", baudrate=9600)
except:
    print("Modbus485**","Failed to write data")
MQTT_TOPIC_AI="/innovation/valvecontroller/ai"
m485 = Modbus485(ser)
relay1_ON  = [1, 6, 0, 0, 0, 255, 201, 138]
relay1_OFF = [1, 6, 0, 0, 0, 0, 137, 202]

relay2_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
relay2_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

relay3_ON  = [3, 6, 0, 0, 0, 255, 200, 104]
relay3_OFF = [3, 6, 0, 0, 0, 0, 136, 40]

soil_temperature =[10, 3, 0, 6, 0, 1, 101, 112]
soil_moisture = [10, 3, 0, 21, 0, 1, 148, 181]

mqtt=MQTTHelper()
# Định nghĩa một hàm xử lý để nhận các thông điệp từ máy chủ MQTT
def receive_callback(message):
    print("Received message:", message)

# Gọi phương thức setRecvCallBack để gán hàm xử lý cho việc nhận thông điệp
mqtt.setRecvCallBack(receive_callback)

while True:
    m485.modbus485_send(relay1_ON)
    time.sleep(1)
    m485.modbus485_read_adc()
    time.sleep(5)
    mqtt.publish(MQTT_TOPIC_AI,"hello")
    # m485.modbus485_send(relay1_OFF)
    # time.sleep(1)
    # m485.modbus485_read_adc()
    # time.sleep(5)

    # m485.modbus485_send(soil_temperature)
    # time.sleep(1)
    # m485.modbus485_read_adc()
    # time.sleep(1)
    # m485.modbus485_send(soil_moisture)
    # time.sleep(1)
    # m485.modbus485_read_adc()
    # time.sleep(1)

