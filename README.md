
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
- [cloudscraper](https://pypi.org/project/cloudscraper/)
- [fake-useragent](https://pypi.org/project/fake-useragent/)
- [loguru](https://loguru.readthedocs.io/)
- [pyfiglet](https://pypi.org/project/pyfiglet/)
- [python-dateutil](https://pypi.org/project/python-dateutil/)
- [termcolor](https://pypi.org/project/termcolor/)

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
   - **`proxies.txt` (optional):** A list of proxies in the format `protocol://user:pass@host:port`. One proxy per line.

2. **Run the Script:**
```bash
python main.py
```

### Optional:
- Choose whether to use proxies when prompted.
- View real-time logs in the terminal, including ping successes, failures, and connection states.

## Need Proxy?
1. Sign up at [Proxies.fo](https://app.proxies.fo/ref/d02516e7-56b3-9a1f-b7ca-1fb08669f7a6).
2. Go to [Plans](https://app.proxies.fo/plans) and only purchase the "ISP plan" (Residential plans don’t work).
3. Top up your balance, or you can directly buy a plan and pay with Crypto!
4. Go to the Dashboard, select your ISP plan, and click "Generate Proxy."
5. Set the proxy format to `protocol://username:password@hostname:port` and choose any number for the proxy count.
6. Paste the proxies into `proxy.txt`.

---

## Configuration

You can adjust the following parameters in the `main.py` file:

- `PING_INTERVAL`: Interval between pings (in seconds).
- `RETRIES_LIMIT`: Maximum retry attempts before declaring a failure.
- API endpoints are specified in the `DOMAIN_API_ENDPOINTS` dictionary.

---

## License

This project is licensed under the [MIT License](LICENSE).
