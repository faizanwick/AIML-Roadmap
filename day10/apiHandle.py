import requests

try:
    response = requests.get(
        url="https://api.github.com/users/faizanwick",
        timeout=0.01
    )

    response.raise_for_status()

    data = response.json()
    print(data["login"])

except requests.exceptions.InvalidURL:
    print("Invalid URL")

except requests.exceptions.ConnectionError:
    print("Server connection failed")

except requests.exceptions.HTTPError as e:
    print("HTTP error: ", e)