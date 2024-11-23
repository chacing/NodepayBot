import requests

url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"

try:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    file_name = "proxies.txt"
    proxies = response.text.replace("\n", "")
    
    with open(file_name, "w") as file:
        file.write(proxies)
    
    print(f"The proxy list has been successfully saved to '{file_name}'.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the proxy list: {e}")
