import paho.mqtt.client as mqtt
import time
# username: servermonitoring
# Pass: ServerMonitoring_wQ1Z3Q5n64
# Topic: /server/monitoring/
# host: mqttserver.tk
# port: 1883

class MQTTHelper:

    MQTT_SERVER = "mqttserver.tk"
    MQTT_PORT = 1883
    MQTT_USERNAME = "innovation"
    MQTT_PASSWORD = "Innovation_RgPQAZoA5N"

    MQTT_TOPIC_SUB_VALVE = "/innovation/valvecontroller/station1"
    MQTT_TOPIC_SUB_PUMP = "/innovation/pumpcontroller/station1"
    MQTT_TOPIC_SUB_SCHEDULELIST="/innovation/valvecontroller/schedulelist1"
    recvCallBack = None

    def mqtt_connected(self, client, userdata, flags, rc):
        print("Connected succesfully!!")
        client.subscribe(self.MQTT_TOPIC_SUB_VALVE)
        client.subscribe(self.MQTT_TOPIC_SUB_PUMP)
        client.subscribe(self.MQTT_TOPIC_SUB_SCHEDULELIST)


        
    def mqtt_subscribed(self, client, userdata, mid, granted_qos):
        print("Subscribed to Topic!!!")


    def mqtt_recv_message(self, client, userdata, message):
        self.recvCallBack(message)

    def __init__(self):

        self.mqttClient = mqtt.Client()
        self.mqttClient.username_pw_set(self.MQTT_USERNAME, self.MQTT_PASSWORD)
        self.mqttClient.connect(self.MQTT_SERVER, int(self.MQTT_PORT), 60)

        # Register mqtt events
        self.mqttClient.on_connect = self.mqtt_connected
        self.mqttClient.on_subscribe = self.mqtt_subscribed
        self.mqttClient.on_message = self.mqtt_recv_message

        self.mqttClient.loop_start()

    def setRecvCallBack(self, func):
        self.recvCallBack = func

    def publish(self, topic, message):
        self.mqttClient.publish(topic, str(message), retain=True)
    


# mqtt=MQTTHelper()
# # Định nghĩa một hàm xử lý để nhận các thông điệp từ máy chủ MQTT
# def receive_callback(message):
#     print("Received message:", message)

# # Gọi phương thức setRecvCallBack để gán hàm xử lý cho việc nhận thông điệp
# mqtt.setRecvCallBack(receive_callback)
# # mqtt.start_listening()

# # # Do other things or keep the program running
# MQTT_TOPIC_AI="/innovation/valvecontroller/ai"
# while True:
#     mqtt.publish(MQTT_TOPIC_AI,"hello")
#     time.sleep(3)
#     pass