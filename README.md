# Agribot365 Dashboard

Agribot365 Dashboard is a real-time sensor data visualization tool for farmers. It displays sensor data from your farm and provides notifications in real-time. The dashboard is built with Streamlit and Firebase.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
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

1. Run the app:
    ```sh
    streamlit run app.py
    ```
2. Open your web browser and go to `http://localhost:8501` to view the dashboard.

## Architecture

The project is structured as follows:

- `app.py`: This is the main file that runs the Streamlit app.
- `auth.py`: This file handles user authentication.
- `realtimedb.py`: This file handles real-time database operations.
- `credential_loader.py`: This file loads Firebase credentials.

The `App` class in `app.py` inherits from the `FirebaseAuthenticator` and `RealtimeDB` classes in `auth.py` and `realtimedb.py`, respectively. This allows the `App` class to use the methods defined in these classes.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) to get started.
