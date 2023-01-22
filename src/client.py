from paho.mqtt.client import Client, connack_string
from src.utils import parsePlainConfig
import time, os, shutil, logging

class MQTTClient:

    """
    Methods:
        - start         ()
        - stop          ()
        - on_connect    (client: any, 
                         user: any, 
                         flag: any, 
                         rc: any)
        - publish       (payload: any)
    """

    def __init__(self, name: str, port=1883):
        self.logger = logging.getLogger()
        self.client_id = name
        self.port = port
        self.rgb = None
        self.buzzer = None
        try:
            samle_cfg_filename = f"cfg/client/mqtt/sample.cfg"
            cfg_filename = f"cfg/client/mqtt/{name}.cfg"
            if not os.path.exists(cfg_filename):
                self.logger.warning(f"'{cfg_filename}' does not exist. Creating cfonfiguration.")
                shutil.copy2(samle_cfg_filename, cfg_filename)
            self.cfg = parsePlainConfig(cfg_filename)
            self.topic = self.cfg["topic_name"]
            self.broker = self.cfg["broker_ip"]
            self.client = Client(client_id=self.client_id)
            self.client.username_pw_set(self.cfg["username"], self.cfg["password"])
            self.client.on_connect = self.on_connect
        except Exception as e:
            raise e
        
    def start(self):
        while True:
            try:
                self.client.connect(self.broker, self.port)
                break
            except Exception as e:
                self.logger.error(f"{e}")
            time.sleep(1)
        self.client.loop_start()

    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()

    def __del__(self):
        self.client.disconnect()
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info(f"Connection result: {connack_string(rc)}")
        if rc == 0:
            self.client.subscribe(self.topic)
        elif rc == 5:
            # Not authorized (incorrect username or password)
            pass

    def publish(self, payload):
        self.client.publish(self.topic, payload=payload)
