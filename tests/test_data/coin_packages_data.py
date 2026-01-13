"""
Невалидные тестовые данные для POST /coin-packages endpoint.
"""

import pytest

# ============================================================================
# НЕВАЛИДНЫЕ COIN_ID (ожидаем 404)
# ============================================================================

INVALID_COIN_IDS = [
    # Неправильный формат UUID
    pytest.param("invalid-uuid", id="not-uuid-format"),
    pytest.param("12345678", id="too-short"),
    pytest.param("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", id="non-hex-chars"),

    # UUID правильного формата, но не существует
    pytest.param("12345678-1234-1234-1234-123456789012", id="non-existent"),
    pytest.param("00000000-0000-0000-0000-000000000000", id="zero-uuid"),
    pytest.param("ffffffff-ffff-ffff-ffff-ffffffffffff", id="max-uuid"),

    # Граничные случаи
    pytest.param("", id="empty"),
    pytest.param(" ", id="space"),
    pytest.param("a" * 100, id="very-long"),

    # Попытки эксплуатации
    pytest.param("'; DROP TABLE coins; --", id="sql-injection"),
    pytest.param("<script>alert('xss')</script>", id="xss-attempt"),
    pytest.param("../../../etc/passwd", id="path-traversal"),
    pytest.param("12345678-1234-1234-1234-123456789012\x00extra", id="null-byte"),
]

# ============================================================================
# НЕВАЛИДНЫЕ PAYMENT_TYPE (ожидаем 400)
# ============================================================================

INVALID_PAYMENT_TYPES = [
    # Неизвестные типы
    pytest.param("invalid_type", id="unknown-type"),
    pytest.param("credit_card", id="similar-but-wrong"),
    pytest.param("paypal", id="unsupported-method"),

    # Неправильный регистр/формат
    pytest.param("BANK_CARD", id="uppercase"),
    pytest.param("Bank Card", id="with-space-and-caps"),
    pytest.param("bank-card", id="hyphen-instead-underscore"),

    # Граничные случаи
    pytest.param("", id="empty"),
    pytest.param(" ", id="space"),
    pytest.param("sbp ", id="trailing-space"),
    pytest.param(" sbp", id="leading-space"),
    pytest.param("sbp\n", id="newline"),
    pytest.param("a" * 1000, id="very-long"),

    # Попытки эксплуатации
    pytest.param("'; DROP TABLE payments; --", id="sql-injection"),
    pytest.param("<img src=x onerror='alert(1)'>", id="xss-attempt"),
    pytest.param("sbp\x00admin", id="null-byte"),
]

# ============================================================================
# НЕВАЛИДНЫЕ RETURN_URL (ожидаем 400)
# ============================================================================

INVALID_RETURN_URLS = [
    # Пустые значения
    pytest.param("", id="empty"),
    pytest.param(" ", id="space"),

    # Невалидный URL формат
    pytest.param("not-url", id="not-url"),
    pytest.param("htp://example.com", id="typo-in-protocol"),
    pytest.param("ht!tp://example.com", id="invalid-chars-in-protocol"),
    pytest.param("//example.com", id="protocol-relative"),

    # Граничные случаи
    pytest.param("https://example.com/" + "x" * 2000, id="extremely-long-url"),
    pytest.param("https://example.com/path with spaces", id="spaces-in-path"),
    pytest.param("https://example.com/path\t", id="tab-in-url"),
    pytest.param("https://example.com\n", id="newline-in-url"),

    # Опасные протоколы
    pytest.param("javascript:alert('xss')", id="javascript-protocol"),
    pytest.param("data:text/html,<script>alert('xss')</script>", id="data-url"),
    pytest.param("file:///etc/passwd", id="file-protocol"),

    # Локальные адреса (часто блокируются)
    pytest.param("http://localhost:8000/callback", id="localhost"),
    pytest.param("http://127.0.0.1/callback", id="loopback-ip"),
    pytest.param("http://192.168.1.1/callback", id="private-ip"),
    pytest.param("http://10.0.0.1/callback", id="private-ip-10"),

    # Попытки эксплуатации
    pytest.param("https://example.com'; DROP TABLE--", id="sql-injection"),
    pytest.param("https://example.com/page?param=<img src=x onerror='alert(1)'>", id="xss-in-query"),
    pytest.param("https://example.com/page\x00admin", id="null-byte"),
]