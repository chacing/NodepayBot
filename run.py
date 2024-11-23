import asyncio
import aiohttp
import time
import random
from loguru import logger
import uuid
import sys
from colorama import Fore, Style, init

init(autoreset=True)

start_text = """
███████╗███╗░░██╗██╗░░░██╗██╗░░██╗██╗░█████╗░
██╔════╝████╗░██║██║░░░██║██║░██╔╝██║██╔══██╗
█████╗░░██╔██╗██║██║░░░██║█████═╝░██║██║░░██║
██╔══╝░░██║╚████║██║░░░██║██╔═██╗░██║██║░░██║
███████╗██║░╚███║╚██████╔╝██║░╚██╗██║╚█████╔╝
╚══════╝╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝╚═╝░╚════╝░   
"""

logger.remove()
logger.add(
    sink=sys.stdout,
    format="<r>[Nodepay]</r> | <white>{time:YYYY-MM-DD HH:mm:ss}</white> | "
           "<level>{level: <8}</level> | <cyan>{line: <4}</cyan> | <white>{message}</white>"
)
logger = logger.opt(colors=True)

PING_INTERVAL = random.uniform(2, 5)  # Randomized interval between ping requests
DOMAIN_API_ENDPOINTS = {
    "SESSION": "http://api.nodepay.ai/api/auth/session",
    "PING": [
        "http://13.215.134.222/api/network/ping",
        "http://18.139.20.49/api/network/ping",
        "http://18.142.29.174/api/network/ping",
        "http://18.142.214.13/api/network/ping",
        "http://52.74.31.107/api/network/ping",
        "http://52.74.35.173/api/network/ping",
        "http://52.77.10.116/api/network/ping",
        "http://3.1.154.253/api/network/ping",
    ],
}

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NodepayExtension/1.0",
    "Accept": "application/json",
    "Referer": "https://app.nodepay.ai",
    "Origin": "chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm",
    "X-Requested-With": "NodepayExtension",
}

# Utility Functions
def load_file(file_path, file_type):
    """Load a file and ensure it's not empty."""
    try:
        with open(file_path) as file:
            lines = [line.strip() for line in file if line.strip()]
        if not lines:
            raise ValueError(f"The {file_type} file is empty or invalid.")
        logger.info(f"{Fore.GREEN}Successfully loaded {len(lines)} {file_type}.{Style.RESET_ALL}")
        return lines
    except FileNotFoundError:
        raise ValueError(f"The {file_type} file was not found.")
    except Exception as e:
        raise ValueError(f"Error loading {file_type}: {e}")

def uuidv4():
    """Generate a UUID v4 as a string."""
    return str(uuid.uuid4())

# Asynchronous Functions
async def call(session, url, data, token, proxy=None):
    """Send a POST request to the specified URL."""
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    try:
        async with session.post(url, json=data, headers=headers, proxy=proxy, timeout=30) as response:
            response.raise_for_status()
            resp_json = await response.json()
            if resp_json.get("code", -1) < 0:
                raise ValueError(f"Invalid API response: {resp_json}")
            return resp_json
    except aiohttp.ClientResponseError as e:
        logger.error(f"{Fore.RED}HTTP Error {e.status}: {e.message}{Style.RESET_ALL}")
    except aiohttp.ClientProxyConnectionError as e:
        message = str(e).split("ssl:")[0].strip()
        logger.error(f"{Fore.RED}Proxy Connection Error: {message}{Style.RESET_ALL}")
    except aiohttp.ClientConnectionError as e:
        message = str(e).split("ssl:")[0].strip()
        logger.error(f"{Fore.RED}Connection Error: {message}{Style.RESET_ALL}")
    except ConnectionResetError as e:
        logger.error(f"{Fore.RED}Connection reset by remote host: {e}{Style.RESET_ALL}")
    except asyncio.TimeoutError:
        logger.error(f"{Fore.RED}Timeout Error: Connection timed out{Style.RESET_ALL}")
    except aiohttp.ServerDisconnectedError:
        logger.error(f"{Fore.RED}Server Disconnected: Connection was terminated{Style.RESET_ALL}")
    except aiohttp.ClientOSError as e:
        logger.error(f"{Fore.RED}Transport Error: {e}{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
    return None

async def ping(session, proxy, token, ping_urls):
    """Send repeated ping requests to the API URLs."""
    ping_index = 0
    while True:
        url = ping_urls[ping_index]
        data = {
            "id": uuidv4(),
            "timestamp": int(time.time()) + random.randint(-5, 5),
        }
        response = await call(session, url, data, token, proxy)
        if response and response.get("code") == 0:
            if proxy:
                logger.success(f"{Fore.GREEN}Ping success using proxy: {proxy}{Style.RESET_ALL}")
            else:
                logger.success(f"{Fore.GREEN}Ping success without proxy.{Style.RESET_ALL}")
        else:
            if proxy:
                logger.warning(f"{Fore.YELLOW}Ping failed using proxy: {proxy}{Style.RESET_ALL}")
            else:
                logger.warning(f"{Fore.YELLOW}Ping failed without proxy.{Style.RESET_ALL}")
        ping_index = (ping_index + 1) % len(ping_urls)
        await asyncio.sleep(PING_INTERVAL)

async def process_token(token, proxies):
    """Process a specific token with the provided proxies or without proxies."""
    async with aiohttp.ClientSession() as session:
        if proxies:
            tasks = [ping(session, proxy, token, DOMAIN_API_ENDPOINTS["PING"]) for proxy in proxies]
        else:
            tasks = [ping(session, None, token, DOMAIN_API_ENDPOINTS["PING"])]
        await asyncio.gather(*tasks)

async def main():
    """Main function to run the application."""
    print(start_text)

    try:
        use_proxy = input(f"{Fore.YELLOW}Do you want to use proxies? (y/n): {Style.RESET_ALL}").strip().lower()
        if use_proxy in ["yes", "y"]:
            proxies = load_file("proxies.txt", "proxies")
        else:
            proxies = []  # No proxies will be used

        tokens = load_file("tokens.txt", "tokens")
    except ValueError as e:
        logger.error(e)
        return

    tasks = [process_token(token, proxies) for token in tokens]
    try:
        await asyncio.gather(*tasks)
    except asyncio.TimeoutError:
        logger.error(f"{Fore.RED}Some tasks failed due to timeout.{Style.RESET_ALL}")

if __name__ == "__main__":
    asyncio.run(main())
