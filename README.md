# Agribot365 Dashboard

Agribot365 Dashboard is a real-time sensor data visualization tool for farmers. It displays sensor data from your farm and provides notifications in real-time. The dashboard is built with Streamlit and Firebase.

> :warning: **NOTE:** This README is currently incomplete and will be updated soon. Please check back later for more information.

## Table of Contents

- [Agribot365 Dashboard](#agribot365-dashboard)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [1. Arduino Setup](#1-arduino-setup)
    - [2. Firebase Configuration and App Setup](#2-firebase-configuration-and-app-setup)
  - [License](#license)
  - [Contributing](#contributing)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/elshadsabziyev/Agribot365.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Agribot365
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
### 1. Arduino Setup
1. Connect the sensors to the Arduino board.
2. Upload the `sensors.ino` sketch to the Arduino board.
3. Connect the Arduino board to your computer using a USB cable.
4. Open the Arduino IDE and go to `Tools > Port` to select the port where the Arduino board is connected.

### 2. Firebase Configuration and App Setup
1. You need to create a Firebase project and download the service account key file. You can follow the instructions [here](https://firebase.google.com/) to create a Firebase project and download the service account key file.
2. To convert JSON to TOML, go to [ConvertSimple](https://convertsimple.com/convert-json-to-toml/) and convert the JSON file to TOML. Copy the TOML content.
3. Create secrets.toml file in the root directory of the project and add TOML content under the `[firebase_auth]` section. Example:
    ```toml
    [firebase_auth]
    type = "service_account"
    project_id = "your-firebase-project-id"
    private_key_id = "your-private-key-id"
    private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
    client_email = "firebase-adminsdk-xyz@your-firebase-project-id.iam.gserviceaccount.com"
    client_id = "your-client-id"
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xyz%40your-firebase-project-id.iam.gserviceaccount.com"
    ```

4. Go to project settings in Firebase and copy the Firebase project ID. Add the project ID to the `secrets.toml` file under the `[firebase_config]` section. Example:
    ```toml
    [firebase_config]
    apiKey = "your-api-key"
    authDomain = "your-firebase-project-id.firebaseapp.com"
    databaseURL = "https://your-firebase-project-id.firebaseio.com"
    projectId = "your-firebase-project-id"
    storageBucket = "your-firebase-project-id.appspot.com"
    messagingSenderId = "your-messaging-sender-id"
    appId = "your-app-id"
    measurementId = "your-measurement-id"
    ```

5. Run the app:
    ```sh
    streamlit run app.py
    ```
6. Open your web browser and go to `http://localhost:8501` to view the dashboard.


## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) to get started.
`