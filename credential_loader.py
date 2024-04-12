import os
from firebase_admin import credentials


class Credentials:
    """
    Class to manage credentials for Firebase and OpenAI.

    Attributes:
        firebase_credentials (service_account.Credentials): Firestore credentials.
        firebase_config (dict): Firebase configuration.
        openai_credentials (str): OpenAI API key.
        db_url (str): URL of the Firebase database.

    Methods:
        get_firestore_credentials: Retrieves the Firestore credentials from the secrets file.
        get_openai_credentials: Retrieves the OpenAI API key from the secrets file.
        get_firebase_config: Retrieves the Firebase configuration from the secrets file.
    """

    def __init__(self) -> None:
        self.firebase_cert = self.make_firebase_cert()
        self.firebase_config = self.get_firebase_config()
        self.openai_credentials = self.get_openai_credentials()
        self.db_url = os.environ["FIREBASE_CONFIG_DATABASEURL"]

    def make_firebase_cert(self) -> credentials.Certificate:
        """
        Retrieves the Firestore credentials from the environment variables.

        Returns:
            credentials (service_account.Credentials): Firestore credentials.
        """
        credentials_dict = {
            "type": os.environ["FIREBASE_AUTH_TYPE"],
            "project_id": os.environ["FIREBASE_AUTH_PROJECT_ID"],
            "private_key_id": os.environ["FIREBASE_AUTH_PRIVATE_KEY_ID"],
            "private_key": os.environ["FIREBASE_AUTH_PRIVATE_KEY"],
            "client_email": os.environ["FIREBASE_AUTH_CLIENT_EMAIL"],
            "client_id": os.environ["FIREBASE_AUTH_CLIENT_ID"],
            "auth_uri": os.environ["FIREBASE_AUTH_AUTH_URI"],
            "token_uri": os.environ["FIREBASE_AUTH_TOKEN_URI"],
            "auth_provider_x509_cert_url": os.environ["FIREBASE_AUTH_AUTH_PROVIDER_X509_CERT_URL"],
            "client_x509_cert_url": os.environ["FIREBASE_AUTH_CLIENT_X509_CERT_URL"],
        }
        return credentials.Certificate(credentials_dict)

    def get_openai_credentials(self) -> str:
        """
        Retrieves the OpenAI API key from the environment variables.

        Returns:
            openai_api_key (str): OpenAI API key.
        """
        return os.environ["OPENAI_OPENAI_API_KEY"]

    def get_firebase_config(self) -> dict:
        """
        Retrieves the Firebase configuration from the environment variables.

        Returns:
            firebase_config (dict): Firebase configuration.
        """
        return {
            "apiKey": os.environ["FIREBASE_CONFIG_APIKEY"],
            "authDomain": os.environ["FIREBASE_CONFIG_AUTHDOMAIN"],
            "projectId": os.environ["FIREBASE_CONFIG_PROJECTID"],
            "storageBucket": os.environ["FIREBASE_CONFIG_STORAGEBUCKET"],
            "messagingSenderId": os.environ["FIREBASE_CONFIG_MESSAGINGSENDERID"],
            "appId": os.environ["FIREBASE_CONFIG_APPID"],
            "measurementId": os.environ["FIREBASE_CONFIG_MEASUREMENTID"],
            "databaseURL": os.environ["FIREBASE_CONFIG_DATABASEURL"],
        }
