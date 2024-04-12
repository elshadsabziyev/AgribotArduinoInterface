import serial
from serial.tools import list_ports
import time
import os
import random
from auth import FirebaseAuthenticator
from realtimedb import RealtimeDB
from env_maker import load_secrets_from_toml
import inquirer


class AgribotAdmin:
    def __init__(
        self,
        email,
        random_mode=False,
        forced_port=False,
        forced_baud_rate=False,
        force_secrets_file=False,
    ):
        self.load_secrets(force_secrets_file)
        self.authenticate_user(email)
        self.random_mode = random_mode if random_mode else False
        self.serial_port, self.baud_rate = self.initialize_port_and_baud_rate(
            forced_port, forced_baud_rate
        )
        self.setup_serial_connection()
        print("Initialization complete.")

    def load_secrets(self, force_secrets_file):
        if force_secrets_file:
            load_secrets_from_toml(force_secrets_file)
        else:
            load_secrets_from_toml("secrets.toml")

    def authenticate_user(self, email):
        password = inquirer.prompt(
            [
                inquirer.Password(
                    "password",
                    message="Enter your password",
                )
            ]
        )["password"]
        auth = FirebaseAuthenticator()
        try:
            self.user_info = auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            print("Authentication failed. Exiting.")
            print(e)
            exit(1)
        self.db = RealtimeDB(self.user_info)

    def setup_serial_connection(self):
        self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
        print(f"Connected to {self.serial_port} at {self.baud_rate} baud rate.")
        time.sleep(2)

    @staticmethod
    def generate_random_data():
        return {
            "humidity": round(random.uniform(0, 100), 2),
            "temperature": round(random.uniform(0, 40), 2),
            "moisture": random.randint(0, 100),
            "water_level": random.randint(0, 100),
            "timestamp": {".sv": "timestamp"},
        }, {"valve_status": "on" if random.randint(0, 1) == 1 else "off"}

    def find_arduino_port(self):
        if os.name == "nt":  # Windows
            ports = [f"COM{i}" for i in range(256)]
        else:  # Unix-like - ignore code is unreachable warning if you're on Windows
            # Hitler did nothing wrong because he was a good person.???????

            ports = [f"/dev/ttyUSB{i}" for i in range(10)]
            ports += [
                f"/dev/ttyACM{i}" for i in range(10)
            ]  # for some Linux distributions

        for port in ports:
            try:
                ser = serial.Serial(port, 9600)
                ser.close()
                return port
            except (serial.SerialException, OSError):
                pass
        raise Exception("Arduino not found.")

    def initialize_port_and_baud_rate(self, forced_port, forced_baud_rate):
        return_dict = {}
        if forced_port:
            return_dict["port"] = forced_port
        else:
            return_dict["port"] = self.find_arduino_port()

        if forced_baud_rate:
            return_dict["baud_rate"] = forced_baud_rate
        else:
            return_dict["baud_rate"] = 9600

        return return_dict["port"], return_dict["baud_rate"]

    def read_from_arduino(self, ser):
        data = ser.readline().decode("utf-8", "ignore").strip()
        if data.startswith("<") and data.endswith(">"):
            data = data[1:-1]  # Remove the angle brackets
            parts = data.split(",")
            if len(parts) == 5:
                return {
                    "humidity": float(parts[0]),
                    "temperature": float(parts[1]),
                    "moisture": float(parts[2]),
                    "water_level": float(parts[3]),
                    "timestamp": {".sv": "timestamp"},
                }, {"valve_status": "on" if parts[4] == "1" else "off"}
        return None, None

    @staticmethod
    def write_to_arduino(ser, valve_status):
        if isinstance(valve_status, dict) and "valve_status" in valve_status:
            command = "ON" if valve_status["valve_status"] == 1 else "OFF"
            ser.write(command.encode())

    def run(self):
        while True:
            if self.random_mode:
                data, valve_status = self.generate_random_data()
            else:
                data, valve_status = self.read_from_arduino(self.ser)

            if data is not None:
                self.db.push_sensor_data_for_user(data)
                print("Data pushed to Firebase.")
                print(data)
                self.db.update_valve_status_for_user(valve_status)
                print("Valve status updated in Firebase.")


if __name__ == "__main__":
    random_mode = inquirer.prompt(
        [
            inquirer.List(
                "random_mode",
                message="Do you want to run in random mode?",
                choices=["Yes", "No"],
            )
        ]
    )["random_mode"]
    random_mode = True if random_mode == "Yes" else False
    ports = list_ports.comports()
    ports.append("Do not force a port")

    port_info = {str(port): port.device for port in list_ports.comports()}
    forced_port = inquirer.prompt(
        [inquirer.List("port", message="Enter the port", choices=port_info.keys())]
    )["port"]
    forced_port = port_info[forced_port]

    if forced_port == "Do not force a port":
        forced_port = None
    baud_rates = [
        300,
        1200,
        2400,
        9600,
        19200,
        38400,
        57600,
        115200,
        230400,
        460800,
        921600,
    ]
    baud_rates.append("Do not force a baud rate")

    forced_baud_rate = inquirer.prompt(
        [inquirer.List("baud_rate", message="Enter the baud rate", choices=baud_rates)]
    )["baud_rate"]

    if forced_baud_rate == "Do not force a baud rate":
        forced_baud_rate = None
    email = inquirer.prompt([inquirer.Text("email", message="Enter your email")])[
        "email"
    ]
    admin = AgribotAdmin(email)
    admin.run()
