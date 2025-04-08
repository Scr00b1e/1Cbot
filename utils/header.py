import base64

def get_headers():
    username = "Админ"
    password = ""

    credentials = f"{username}:{password}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

    return headers