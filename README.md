# Streamlit Event Tracker

This project is a Streamlit application designed to track events and calculate the time elapsed since the last event of a specific type. The application uses a JSON file to store event data and provides a simple interface for loading, saving, and analyzing this data.

## Features

- Load and save event data from/to a JSON file.
- Calculate the time elapsed since the last event of a specific type.
- Display data using Pandas and Altair for visualization.
- Automatically refresh the Streamlit app using `streamlit_autorefresh`.

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- Altair
- Pytz

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/MalgoCoder54/BabyMonitor
    cd BabyMonitor
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

2. The application will open in your default web browser. You can interact with the interface to load, save, and analyze event data.

## File Structure

- `app.py`: Main application file containing the Streamlit app logic.
- `data.json`: JSON file used to store event data.
- `requirements.txt`: List of required Python packages.

## Functions

### `load_data()`
Loads event data from `data.json`. Returns an empty list if the file does not exist.

### `save_data(data)`
Saves the provided data to `data.json`.

### `time_since_last_event(data, event_type)`
Calculates the time elapsed since the last event of the specified type. Returns the time difference in hours and minutes.

## License

This project is licensed under the GNU GPL License. See the [GNU GPL WEBSITE](https://www.gnu.org/licenses/gpl-3.0.en.html) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

## Contact

For any questions or suggestions, please contact [me]() ok linkdin.
