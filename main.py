import asyncio
import json
import sys
import time
import uuid
from fake_useragent import UserAgent
from curl_cffi import requests
from loguru import logger
from pyfiglet import figlet_format
from termcolor import colored
from urllib.parse import urlparse

# Constants
PING_INTERVAL = 0.5
DOMAIN_API = {
    "SESSION": "http://api.nodepay.ai/api/auth/session",
    "PING": ["http://18.142.29.174/api/network/ping", "https://nw.nodepay.org/api/network/ping"]
}

# Logger Setup
logger.remove()
logger.add(
    sink=sys.stdout,
    format="<r>[Nodepay]</r> | <white>{time:YYYY-MM-DD HH:mm:ss}</white> | "
           "<level>{level: <7}</level> | <cyan>{line: <3}</cyan> | {message}",
    colorize=True
)

# Print header with pyfiglet
def print_header():
    ascii_art = figlet_format("NodepayBot", font="slant")
    colored_art = colored(ascii_art, color="cyan")
    border = "=" * 40
    print(border)
    print(colored_art)
    print("Welcome to NodepayBot - Automate your tasks effortlessly!")
    print(border)

# Read tokens and proxies
def read_tokens_and_proxy():
    try:
        with open('tokens.txt', 'r') as file:
            tokens_count = sum(1 for line in file if line.strip())

        with open('proxies.txt', 'r') as file:
            proxies_count = sum(1 for line in file if line.strip())

        return tokens_count, proxies_count
    except FileNotFoundError as e:
        logger.error(f"File not found: {e.filename}")
        return 0, 0

# Ask user if they want to use proxies
def ask_user_for_proxy():
    user_input = ""
    while user_input not in ['yes', 'no']:
        user_input = input("Do you want to use proxy? (yes/no)? ").strip().lower()
        if user_input not in ['yes', 'no']:
            print(colored("Invalid input. Please enter 'yes' or 'no'.", "red"))
    print(f"You selected: {'Yes' if user_input == 'yes' else 'No'}")
    return user_input == 'yes'

# Load proxies from file
def load_proxies():
    try:
        with open('proxies.txt', 'r') as file:
            proxies = file.read().splitlines()
        return proxies
    except FileNotFoundError:
        logger.error("File proxies.txt not found. Please create it.")
        return []

# Call API function
async def call_api(url, data, token, proxy=None):
    user_agent = UserAgent().chrome if UserAgent().chrome else "Mozilla/5.0"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": user_agent,
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json"
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        response = requests.post(url, json=data, headers=headers, proxies=proxies, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during API call: {repr(e)}")
        return None

# Start pinging API
async def start_ping(token, account_info, proxy):
    browser_id = str(uuid.uuid4())
    url_index = 0
    while True:
        try:
            url = DOMAIN_API["PING"][url_index]
            data = {
                "id": account_info.get("uid"),
                "browser_id": browser_id,
                "timestamp": int(time.time())
            }
            response = await call_api(url, data, token, proxy)
            if response:
                response_data = response.get("data", {})
                ip_score = response_data.get("ip_score", "Unavailable")
                logger.info(f"<green>Ping Successful</green>, IP Score: <cyan>{ip_score}</cyan>")
            else:
                logger.warning(f"<yellow>No response from {url}</yellow>")
        except Exception as e:
            logger.error(f"Unhandled exception: {repr(e)}")
        finally:
            await asyncio.sleep(PING_INTERVAL)
            url_index = (url_index + 1) % len(DOMAIN_API["PING"])

# Process account
async def process_account(token, use_proxy, proxies=None):
    proxies = proxies or []
    for proxy in (proxies if use_proxy else [None]):
        try:
            response = await call_api(DOMAIN_API["SESSION"], {}, token, proxy)
            if response and response.get("code") == 0:
                account_info = response["data"]
                logger.info(f"Account: {account_info.get('name', 'Unknown')}")
                await start_ping(token, account_info, proxy)
                return
            else:
                logger.warning(f"<yellow>Invalid or no response for token with proxy {proxy}</yellow>")
        except Exception as e:
            logger.error(f"Unhandled error with proxy {proxy}: {repr(e)}")
    logger.error(f"<yellow>All attempts failed for token</yellow>")

# Main function
async def main():
    print_header()

    tokens_count, proxies_count = read_tokens_and_proxy()
    print(colored(f"Tokens: {tokens_count}", "green"))
    print(colored(f"Proxies: {proxies_count}", "cyan"))
    print(colored("Nodepay supports only 3 connections per account.", "yellow"))
    print("=" * 40)

    use_proxy = ask_user_for_proxy()
    proxies = load_proxies() if use_proxy else []

    try:
        with open('tokens.txt', 'r') as file:
            tokens = file.read().splitlines()
    except FileNotFoundError:
        print(colored("File tokens.txt not found. Please create it.", "red"))
        exit()

    tasks = []
    for token in tokens:
        tasks.append(process_account(token, use_proxy, proxies))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Task for token {tokens[i]} failed: {repr(result)}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Program terminated by user.")
