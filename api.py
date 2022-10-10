import requests
import json


class API:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_endpoint_v2(self, endpoint: str):
        url = f"https://api.guildwars2.com/v2/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        return requests.get(url, headers=headers).json()

    def check_key(self) -> bool:
        # Check if api key is valid
        tokeninfo = self.get_endpoint_v2("tokeninfo")
        if "Invalid access token" in str(tokeninfo):
            return False

        # Check if correct permissions are set
        perms = tokeninfo["permissions"]
        if "account" not in perms:  # Should always be set but check anyway
            return False
        if "progression" not in perms:
            return False
        if "characters" not in perms:
            return False
        return True

    def get_account_name(self) -> str:
        account = self.get_endpoint_v2("account")
        return account["name"]

    def get_characters(self) -> list[str]:
        return self.get_endpoint_v2("characters")


if __name__ == "__main__":
    api = API("API_KEY")
    print("Key valid:", api.check_key())
    print("Account Name:", api.get_account_name())
    print("Characters:", api.get_characters())
