
# Nodepay Ping Utility

The Nodepay Ping Utility is an asynchronous Python-based tool designed to send ping requests to multiple API endpoints, with support for proxies. It features colored logging for tracking status and robust error handling for network issues.

## Features

- **Asynchronous Processing:** Utilizes `asyncio` and `aiohttp` for parallel request handling.
- **Proxy Support:** Option to use a proxy list from `proxies.txt`.
- **Logging:** Provides colored logs using `loguru` and `colorama`.
- **Randomized Ping Intervals:** Adds a random interval between each ping request.
- **Error Handling:** Handles various network errors and provides detailed logs.

## Get NP_TOKEN
Retrieving `np_token`: A quick guide to find your `np_token`:

- Open the webpage in your browser.
- Press `F12` or use `Ctrl + Shift + I` (Windows/Linux) / `Cmd + Option + I` (Mac) to open the developer console.
- Go to the **Console** tab.
- Enter the following command:

     ```javascript
     localStorage.getItem('np_token');
     ```
- The value displayed is your `np_token`.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Enukio/Nodepay.git
   ```
   ```bash
   cd Nodepay
   ```

2. Ensure Python 3.7 or higher is installed, then install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare Configuration Files:**
   - **`tokens.txt`:** A list of tokens for API authentication. One token per line.
   - **`proxies.txt` (optional):** A list of proxies in the format `http://user:password@host:port`. One proxy per line.
     - You can generate this file using the `getproxies.py` script.

2. **Generate Proxy List (Optional):**
   - Run `getproxies.py` to download and save free proxies:

     ```bash
     python getproxies.py
     ```
   - This will save the proxy list to `proxies.txt` in the current directory.

3. **Run the Script:**
   ```bash
   python run.py
   ```

4. **Follow the Instructions:**
   - The script will prompt you to choose whether to use proxies.

## Script Overview

- **Constants:**
  - `DOMAIN_API_ENDPOINTS`: Contains API endpoints to ping.
  - `HEADERS`: Default headers for API requests.
  
- **Utility Functions:**
  - `load_file`: Loads configuration files like `tokens.txt` and `proxies.txt`.
  - `uuidv4`: Generates a unique UUID v4 for each request.

- **Async Functions:**
  - `call`: Sends a POST request to an API endpoint.
  - `ping`: Performs repeated ping requests to endpoints.
  - `process_token`: Processes a single token with or without proxies.
  - `main`: The main function to start the application.

## Dependencies

- [aiohttp](https://docs.aiohttp.org/)
- [loguru](https://loguru.readthedocs.io/)
- [colorama](https://pypi.org/project/colorama/)
- [requests](https://docs.python-requests.org/) (for `getproxies.py`)

## License

This project is licensed under the [MIT License](LICENSE).
