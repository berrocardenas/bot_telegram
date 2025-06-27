import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class HotmartService:
    def __init__(self):
        self.token = os.getenv("HOTMART_TOKEN")
        self.api_url = "https://api.hotmart.com/v1/sales/history"

    def get_user_status(self, email: str) -> dict:
        """Verifica si el usuario está activo en Hotmart."""
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"buyer_email": email}

        try:
            response = requests.get(self.api_url, headers=headers, params=params)
            data = response.json()

            if not data.get("sales"):
                return {"active": False, "message": "❌ Correo no registrado en Hotmart."}

            # Verificar vigencia (1 año desde la última compra)
            last_purchase = data["sales"][0]
            purchase_date = datetime.strptime(
                last_purchase["purchase_date"], "%Y-%m-%d %H:%M:%S"
            )
            expiry_date = purchase_date + timedelta(days=365)

            if datetime.now() > expiry_date:
                return {
                    "active": False,
                    "message": f"⚠️ Tu acceso expiró el {expiry_date.strftime('%d/%m/%Y')}",
                }
            else:
                return {
                    "active": True,
                    "message": f"✅ Acceso válido hasta el {expiry_date.strftime('%d/%m/%Y')}",
                }

        except Exception as e:
            return {"active": False, "message": "🔴 Error al conectar con Hotmart."}
    
