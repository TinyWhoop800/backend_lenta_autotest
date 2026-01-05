import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BASE_URL = os.getenv("API_BASE_URL", "https://lenta-test.iptv2021.com/api/v1")

settings = Settings()