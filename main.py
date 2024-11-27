import asyncio
import re
import sys
import time
import uuid

from fake_useragent import UserAgent
from loguru import logger
import aiohttp
from pyfiglet import figlet_format
from termcolor import colored

# Konfigurasi logger
logger.remove()
logger.add(
    sink=sys.stdout,
    format="<r>[Nodepay]</r> | <white>{time:YYYY-MM-DD HH:mm:ss}</white> | "
           "<level>{level: <7}</level> | <cyan>{line: <3}</cyan> | {message}",
    colorize=True,
    level="DEBUG"
)

# Header aplikasi
def print_header():
    ascii_art = figlet_format("NodepayBot", font="slant")
    colored_art = colored(ascii_art, color="cyan")
    border = "=" * 60
    print(border)
    print(colored_art)
    print("Welcome to NodepayBot - Automate your tasks effortlessly!")
    print(border)

print_header()

# Fungsi membaca token dan proxy
def read_tokens_and_proxy():
    with open('tokens.txt', 'r') as file:
        tokens_content = sum(1 for line in file)

    with open('proxy.txt', 'r') as file:
        proxy_count = sum(1 for line in file)

    return tokens_content, proxy_count

tokens_content, proxy_count = read_tokens_and_proxy()

print()
print(f"Tokens: {tokens_content}. | Loaded {proxy_count} proxies.\n")
print(f"Nodepay only supports 3 connections per account. Using too many proxies may cause issues.")
print()
print("=" * 60)

HIDE_PROXY = "[HIDDEN]"
PING_INTERVAL = 1
RETRIES_LIMIT = 60

# Endpoint API
DOMAIN_API_ENDPOINTS = {
    "SESSION": [
        "https://api.nodepay.ai/api/auth/session"
    ],
    "PING": [
        "http://13.215.134.222/api/network/ping"
    ]
}

CONNECTION_STATES = {
    "CONNECTED": 1,
    "DISCONNECTED": 2,
    "NO_CONNECTION": 3
}

status_connect = CONNECTION_STATES["NO_CONNECTION"]
browser_id = None
account_info = {}
last_ping_time = {}

# Fungsi utilitas
def generate_uuid():
    return str(uuid.uuid4())

def validate_response(response):
    if not response or "code" not in response or response["code"] < 0:
        raise ValueError("Invalid response received from the server.")
    return response

async def send_request(url, payload, proxy, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": UserAgent().random,
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://app.nodepay.ai",
        "Origin": "chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm",
        "X-Requested-With": "NodepayExtension",
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload, headers=headers, proxy=proxy, timeout=60) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"<yellow>API Request Failed: {str(e)}</yellow>")
            raise

async def send_ping(proxy, token):
    global last_ping_time, RETRIES_LIMIT, status_connect
    last_ping_time[proxy] = time.time()

    try:
        data = {
            "id": account_info.get("uid"),
            "browser_id": browser_id,
            "timestamp": int(time.time())
        }

        response = await send_request(DOMAIN_API_ENDPOINTS["PING"][0], data, proxy, token)
        validate_response(response)

        ip_address = re.search(r'(?<=@)[^:]+', proxy).group() if proxy else HIDE_PROXY
        logger.success(f"<green>Ping Successful</green>, IP Score: <cyan>{response['data'].get('ip_score')}</cyan>, Proxy: <yellow>{ip_address}</yellow>")
        
        RETRIES_LIMIT = 0  # Reset retry limit jika berhasil
        status_connect = CONNECTION_STATES["CONNECTED"]

    except aiohttp.ClientError as e:
        RETRIES_LIMIT += 1
        logger.error(f"<red>Ping failed due to network error</red>: {e}")
        if RETRIES_LIMIT > 10:
            logger.error(f"Max retry limit reached. Removing Proxy: {proxy}.")
            remove_proxy(proxy)
            status_connect = CONNECTION_STATES["DISCONNECTED"]
        else:
            logger.warning(f"<yellow>Retrying Ping... Attempt {RETRIES_LIMIT}/10</yellow>")
    
    except asyncio.TimeoutError:
        RETRIES_LIMIT += 1
        logger.warning(f"<yellow>Ping timeout. Retrying... Attempt {RETRIES_LIMIT}/10</yellow>")
        if RETRIES_LIMIT > 10:
            logger.error(f"Max retry limit reached. Removing Proxy: {proxy}.")
            remove_proxy(proxy)
            status_connect = CONNECTION_STATES["DISCONNECTED"]
    
    except ValueError as ve:
        RETRIES_LIMIT += 1
        logger.error(f"<red>Invalid response during ping</red>: {ve}")
        if RETRIES_LIMIT > 10:
            logger.error(f"Max retry limit reached. Removing Proxy: {proxy}.")
            remove_proxy(proxy)
            status_connect = CONNECTION_STATES["DISCONNECTED"]

    except Exception as e:
        RETRIES_LIMIT += 1
        logger.error(f"<red>Unexpected error during ping</red>: {e}")
        if RETRIES_LIMIT > 10:
            logger.error(f"Max retry limit reached. Removing Proxy: {proxy}.")
            remove_proxy(proxy)
            status_connect = CONNECTION_STATES["DISCONNECTED"]

async def main():
    use_proxy = ask_user_for_proxy()

    proxies = load_proxies('proxy.txt') if use_proxy else []

    try:
        with open('tokens.txt', 'r') as file:
            tokens = file.read().splitlines()
    except FileNotFoundError:
        logger.error(f"tokens.txt not found. Ensure the file is in the correct directory.")
        exit()

    if not tokens:
        logger.error(f"No tokens provided. Exiting.")
        exit()

    token_proxy_pairs = [(tokens[i % len(tokens)], proxy) for i, proxy in enumerate(proxies)] if use_proxy else [(token, "") for token in tokens]

    tasks = [asyncio.create_task(initialize_profile(proxy, token)) for token, proxy in token_proxy_pairs]

    while True:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Task encountered an error")
            else:
                logger.success(f"Task completed successfully")

        await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning(f"Program terminated by user.")
