
# NodepayBot - Ping Utility

NodepayBot is a Python-based tool designed to automate tasks for the Nodepay service, featuring token and proxy management, API interaction, and connection monitoring. This bot makes use of asynchronous programming for efficient operations and ensures a smooth automation experience.

---

## Features

- **Automated API Interactions**: Handles session initialization, pings, and connection states.
- **Proxy Support**: Enables using proxies for improved security and anonymity.
- **Token Management**: Reads and utilizes tokens for authenticated interactions.
- **Logging**: Real-time and colorful logs powered by `loguru` for better debugging and monitoring.
- **Customizable Settings**: Adjustable ping intervals and retry limits.

---

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
- Save `np_token` to `tokens.txt`

---

## Requirements

Ensure you have Python 3.8 or newer installed.

Install the required dependencies:
```bash
pip install -r requirements.txt
```

Dependencies include:
- [asyncio](https://pypi.org/project/asyncio/)
- [aiohttp](https://docs.aiohttp.org/)
- [fake_useragent](https://pypi.org/project/fake-useragent/)
- [pyfiglet](https://pypi.org/project/pyfiglet/)
- [termcolor](https://pypi.org/project/termcolor/)
- [loguru](https://loguru.readthedocs.io/)
- [requests](https://docs.python-requests.org/) (for `getproxies.py`)

---

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Enukio/NodepayBot.git
   ```
   ```bash
   cd NodepayBot
   ```

2. Place your API tokens in a file named `tokens.txt` (one token per line).

3. If using proxies, create a file named `proxy.txt` and list your proxies (one per line).

---

## Usage
1. **Prepare Configuration Files:**
   - **`tokens.txt`:** A list of tokens for API authentication. One token per line.
   - **`proxies.txt` (optional):** A list of proxies in the format `type://user:password@host:port` or `type://host:port`. One proxy per line.
     - You can generate this file using the `getproxies.py` script.

2. **Generate Proxy List (Optional):**
   - Run `getproxies.py` to download and save free proxies:

     ```bash
     python getproxies.py
     ```
   - This will save the proxy list to `proxies.txt` in the current directory.

3. **Run the Script:**
```bash
python main.py
```

### Optional:
- Choose whether to use proxies when prompted.
- View real-time logs in the terminal, including ping successes, failures, and connection states.

---

## Configuration

You can adjust the following parameters in the `main.py` file:

- `PING_INTERVAL`: Interval between pings (in seconds).
- `RETRIES_LIMIT`: Maximum retry attempts before declaring a failure.
- API endpoints are specified in the `DOMAIN_API_ENDPOINTS` dictionary.

---

## License

This project is licensed under the [MIT License](LICENSE).
