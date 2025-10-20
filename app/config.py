API_URL = "https://wigorservices/api/schedule"
API_BASE_URL = "https://api.wigorservices.net/"
TIMEOUT = 10

def get_headers(cookie: str) -> dict:
    return {
        "Cookie": f"session={cookie}",
        "Accept": "application/json"
    }
