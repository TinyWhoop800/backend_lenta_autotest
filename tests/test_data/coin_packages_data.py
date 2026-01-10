"""Тестовые данные для POST /coin_packages"""

# Невалидные coin_id для 404
INVALID_COIN_IDS = [
    "00000000-0000-0000-0000-000000000000",
    "invalid-uuid",
    "12345678-1234-1234-1234-123456789012",
]

# Невалидные payment_type для 400
INVALID_PAYMENT_TYPES = ["invalid", "", "BANK_CARD"]
