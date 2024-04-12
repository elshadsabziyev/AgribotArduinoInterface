from credential_loader import Credentials
import firebase


class RealtimeDB(Credentials):
    """
    A class representing a Realtime Database.

    Inherits from the Credentials class.

    Attributes:
        app: The Firebase app instance.
        auth: The Firebase authentication instance.
        db: The Firebase database instance.
        user_info: The user information such as the localId and idToken.
        id_token: The ID token of the user, used for authentication.

    Methods:
        push_sensor_data_for_user: Pushes new sensor data for the user.
        update_valve_status_for_user: Updates the valve_status for the user.
        delete_sensor_data_for_user: Deletes all the sensor data for the user.
    """

    def __init__(self, user_info) -> None:
        super().__init__()
        try:
            self.app = firebase.initialize_app(self.firebase_config)
        except Exception as e:
            raise Exception("There was an error initializing the Firebase app.")
        self.db = self.app.database()
        self.user_info = user_info
        self.id_token = user_info["idToken"]

    def push_sensor_data_for_user(self, data: dict) -> None:
        """
        Sets the sensor data for the user.

        Args:
            data (dict): The sensor data to set.

        Returns:
            None
        """
        try:
            uid = self.user_info["localId"]
            self.db.child("users").child(uid).child("sensor_data").push(
                data=data, token=self.id_token
            )
        except Exception as e:
            raise Exception("There was an error pushing the sensor data.")

    def update_valve_status_for_user(self, valve_status: str) -> None:
        """
        Updates the valve_status for the user.

        Args:
            valve_status (str): The new valve_status value.

        Returns:
            None
        """
        try:
            uid = self.user_info["localId"]

            # Update the valve_status field under the user's uid
            self.db.child("users").child(uid).child("valve_status").set(
                valve_status, token=self.id_token
            )
        except Exception as e:
            raise Exception("There was an error updating the valve status.")

    def delete_sensor_data_for_user(self) -> None:
        """
        Deletes all the sensor data for the user.
        Also deletes the valve_status field for the user.

        Returns:
            None
        """
        try:
            uid = self.user_info["localId"]
            self.db.child("users").child(uid).child("sensor_data").remove(
                token=self.id_token
            )
            self.db.child("users").child(uid).child("valve_status").remove(
                token=self.id_token
            )
        except Exception as e:
            raise Exception("There was an error deleting the sensor data.")
