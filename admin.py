import serial
from serial.tools import list_ports
import time
import os
import random
from auth import FirebaseAuthenticator
from realtimedb import RealtimeDB
from env_maker import load_secrets_from_toml
import inquirer
import rich
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.table import Table


class AgribotAdmin:

    def __init__(
        self, email, random_mode, forced_port, forced_baud_rate, forced_secrets_file
    ):
        self.console = Console()

        self.load_secrets(forced_secrets_file)
        self.authenticate_user(email)
        self.setup_serial_connection(random_mode, forced_port, forced_baud_rate)
        self.random_mode = random_mode
        self.console.print(
            Panel(
                "Welcome to the Agribot Admin Panel!",
                title="Agribot Admin",
                style="bold green",
            )
        )
        self.table = Table(show_header=True, header_style="bold green")
        self.table.add_column("Parameter", style="dim", width=12)
        self.table.add_column("Value", justify="right")
        self.table.add_row("No data", "No data")
        self.live = Live(self.table, refresh_per_second=4)

    def load_secrets(self, forced_secrets_file):

        if forced_secrets_file:
            load_secrets_from_toml(forced_secrets_file)
        else:
            load_secrets_from_toml("secrets.toml")

    def authenticate_user(self, email):

        password = inquirer.prompt(
            [
                inquirer.Password(
                    "password",
                    message="Enter your password",
                    validate=lambda _, response: len(response) >= 6,
                    echo=f"{random.choice(['*', '🌱', '🌿', '🍃', '🔑'])}",
                )
            ]
        )["password"]
        auth = FirebaseAuthenticator()
        try:
            self.user_info = auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            self.console.print_exception(show_locals=True)
            self.console.print("[bold red]Authentication failed. Exiting.")
            exit(1)
        self.db = RealtimeDB(self.user_info)

    def setup_serial_connection(self, random_mode, forced_port, forced_baud_rate):

        if not random_mode:
            if not forced_port:
                serial_port = self.find_arduino_port()
            else:
                serial_port = forced_port
            if not forced_baud_rate:
                baud_rate = 9600
            else:
                baud_rate = forced_baud_rate
            self.ser = serial.Serial(serial_port, baud_rate, timeout=1)
            self.console.print(
                f"[bold green]Serial connection established with {serial_port} at {baud_rate} baud."
            )

            time.sleep(2)
        else:
            self.console.print(
                Panel(
                    "[bold green]Random mode enabled. No serial connection needed.",
                    style="green",
                )
            )

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

    def run(self):
        with self.live as live:  # Enter the Live context
            while True:
                if self.random_mode:
                    data, valve_s = self.generate_random_data()
                else:
                    data, valve_s = self.read_from_arduino(self.ser)

                if data is not None:
                    # Create a new table for each iteration
                    self.table = Table(show_header=True, header_style="bold magenta")
                    self.table.add_column("Parameter")
                    self.table.add_column("Value")

                    # Update the table
                    self.table.add_row("Humidity", f"{data['humidity']}%")
                    self.table.add_row("Temperature", f"{data['temperature']}°C")
                    self.table.add_row("Moisture", f"{data['moisture']}%")
                    self.table.add_row("Water Level", f"{data['water_level']}%")
                    self.table.add_row("Valve Status", valve_s["valve_status"])

                    live.update(self.table)  # Update the Live output with the new table
                    self.db.push_sensor_data_for_user(data)
                    self.db.update_valve_status_for_user(valve_s["valve_status"])
                    time.sleep(1)


if __name__ == "__main__":
    console = Console()
    random_mode = inquirer.prompt(
        [
            inquirer.List(
                "random_mode",
                message="Do you want to run in random mode?",
                choices=["Yes", "No"],
                carousel=True,
                default="No",
            )
        ]
    )["random_mode"]
    random_mode_text = Text(
        f"{'Random mode is enabled' if random_mode == 'Yes' else 'Random mode is disabled'}",
        style="bold green" if random_mode == "Yes" else "bold red",
    )
    console.print(Panel(random_mode_text, style="green" if random_mode else "red"))
    random_mode = True if random_mode == "Yes" else False
    if not random_mode:
        forced_port = inquirer.prompt(
            [
                inquirer.List(
                    "port",
                    message="Enter the port to use for communication with Arduino (Defaults to 9600)",
                    choices=list_ports.comports() + ["Do not force a port"],
                    carousel=True,
                    default="Do not force a port",
                )
            ]
        )["port"]
        forced_port = (
            str(forced_port).split(" ")[0]
            if forced_port != "Do not force a port"
            else False
        )
        port_text = Text(
            f"{forced_port + ' is selected as the port' if forced_port else 'First available port will be used as the port'}",
            style="bold green",
        )
        console.print(Panel(port_text, style="green"))
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

        forced_baud_rate = inquirer.prompt(
            [
                inquirer.List(
                    "baud_rate",
                    message="Enter the baud rate to use for communication with Arduino (Defaults to 9600)",
                    choices=baud_rates + ["Do not force a baud rate"],
                    carousel=True,
                    default="Do not force a baud rate",
                )
            ]
        )["baud_rate"]

        if forced_baud_rate == "Do not force a baud rate":
            forced_baud_rate = False
        baud_rate_text = Text(
            f"{forced_baud_rate if forced_baud_rate else 9600} is selected as the baud rate",
            style="bold green",
        )
        console.print(Panel(baud_rate_text, style="green"))
    else:
        forced_port = False
        forced_baud_rate = False
        console.print(
            Panel(
                "[bold green]No port or baud rate needed.[/bold green]",
                style="green",
            )
        )

    force_secrets_file = inquirer.prompt(
        [
            inquirer.Text(
                "secrets_file",
                message="Enter the name of the secrets file (Defaults to secrets.toml)",
                default="secrets.toml",
            )
        ]
    )["secrets_file"]
    secrets_file_text = Text(
        f"{force_secrets_file + ' is selected as the secrets file' if force_secrets_file else 'secrets.toml will be used as the secrets file'}",
        style="bold green",
    )
    console.print(Panel(secrets_file_text, style="green"))

    email = inquirer.prompt([inquirer.Text("email", message="Enter your email")])[
        "email"
    ]
    admin = AgribotAdmin(
        email, random_mode, forced_port, forced_baud_rate, force_secrets_file
    )
    admin.run()
