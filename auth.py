import json
import requests
from credential_loader import Credentials
import re


class FirebaseAuthenticator(Credentials):
    """
    Class to manage user authentication using Firebase.

    Attributes:
        firebase_config (str): Firebase configuration.

    Methods:
        sign_in_with_email_and_password: Signs in a user with the provided email and password.
        get_account_info: Retrieves the account information associated with the given ID token.
        raise_detailed_error: Raises a detailed error if the HTTP request returns an error status code.
        sign_in: Signs in a user with the provided email and password.
    """

    def __init__(self) -> None:
        super().__init__()
        self.firebase_config = self.get_firebase_config().get("apiKey")
        self.current_user = (
            None  # Add this line to keep track of the currently signed-in user
        )

    def sign_in_with_email_and_password(self, email: str, password: str) -> dict:
        """
        Signs in a user with the provided email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            dict: A dictionary containing the response data from the API.

        Raises:
            DetailedError: If there is an error during the API request.
        """
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(
            self.firebase_config
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps(
            {"email": email, "password": password, "returnSecureToken": True}
        )
        request_object = requests.post(request_ref, headers=headers, data=data)
        self.raise_detailed_error(request_object)
        return request_object.json()

    def get_account_info(self, id_token: str) -> dict:
        """
        Retrieves the account information associated with the given ID token.

        Args:
            id_token (str): The ID token to authenticate the request.

        Returns:
            dict: The account information as a dictionary.

        Raises:
            DetailedError: If there is an error in the request.
        """
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={0}".format(
            self.firebase_config
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"idToken": id_token})
        request_object = requests.post(request_ref, headers=headers, data=data)
        self.raise_detailed_error(request_object)
        return request_object.json()

    def raise_detailed_error(self, request_object: requests.models.Response) -> None:
        """
        Raises a detailed error if the HTTP request returns an error status code.

        Args:
            request_object (requests.models.Response): The response object from the HTTP request.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returns an error status code.

        """
        try:
            request_object.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise requests.exceptions.HTTPError(error, request_object.text)

    def sign_in(self, email: str, password: str) -> None:
        """
        Signs in a user with the provided email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Raises:
            requests.exceptions.HTTPError: If there is an HTTP error during the sign-in process.
            Exception: If there is an error during the sign-in process.

        Returns:
            None
        """
        try:
            id_token = self.sign_in_with_email_and_password(email, password)["idToken"]
            account_info = self.get_account_info(id_token)
            user_info = account_info["users"][0]
            if not user_info["emailVerified"]:
                self.send_email_verification(id_token)
                print(
                    """
                ##### Email not verified.
                - Check your inbox to verify your email.
                - Please check your spam folder if you don't see it in your inbox.
                """
                )
            else:
                user_info["idToken"] = id_token
                user_info["fullUserInfo"] = account_info
                print("User signed in successfully.")
        except requests.exceptions.HTTPError as error:
            error_message = json.loads(error.args[1])["error"]["message"]
            if error_message in {
                "INVALID_EMAIL",
                "EMAIL_NOT_FOUND",
                "INVALID_PASSWORD",
                "MISSING_PASSWORD",
                "INVALID_LOGIN_CREDENTIALS",
            }:
                print(
                    """
                ##### Error: Invalid login credentials.
                - Please check your email and password.
                - Forgot your password?
                - Click the 'Forgot Password' button to reset it.
                """
                )
            elif any(
                re.search(pattern, error_message, re.IGNORECASE)
                for pattern in {
                    "TOO_MANY_ATTEMPTS_TRY_LATER",
                    "USER_DISABLED",
                    "OPERATION_NOT_ALLOWED",
                    "USER_NOT_FOUND",
                    "TOO_MANY_ATTEMPTS_TRY_LATER : Too many unsuccessful login attempts. Please try again later.",
                }
            ):
                print(
                    """
                ##### Error: Too many attempts.
                - Please try again later.
                - You are temporarily blocked from signing in.
                - Be sure to verify your email.
                - Get access instantly by resetting your password.
                - Or, wait for a while and try again.
                """
                )
            else:
                print(f"Error: {error_message}")
        except Exception as error:
            print(f"Error: {error}")
