import requests
import os
from dotenv import load_dotenv

load_dotenv()

async def verify_hotmart_user(email: str) -> bool:
    try:
        response = requests.get(
            "https://api.hotmart.com/v1/users/check",
            params={"email": email},
            headers={"Authorization": f"Bearer {os.getenv('HOTMART_TOKEN')}"}
        )
        return response.json().get("is_buyer", False)
    except Exception as e:
        print(f"Error al verificar en Hotmart: {e}")
        return False