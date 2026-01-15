"""
Невалидные тестовые данные для GET /contents/...
"""

import pytest

# ============================================================================
# НЕВАЛИДНЫЕ CONTENT_ID (ожидаем 404)
# ============================================================================

INVALID_CONTENT_IDS = [
    # Граничные значения для целых чисел
    pytest.param(9223372036854775807, id="max_int64"),
    pytest.param(-9223372036854775808, id="min_int64"),

    # Буквы и спец символы
    pytest.param("abc", id="letters_only"),
    pytest.param("12.34", id="float_like"),
    pytest.param("12a34", id="mixed_alphanum"),

    # Пустые значения
    pytest.param(" ", id="single_space"),

    # Очень длинные значения
    pytest.param("a" * 1000, id="very_long_1000"),

    # Unicode и спец символы
    pytest.param("Ñ", id="unicode_special"),
    pytest.param("😀", id="emoji"),
    pytest.param("\\u0000", id="null_unicode"),

    # Попытки эксплуатации
    pytest.param("'; DROP TABLE collections; --", id="sql-injection"),
    pytest.param("<script>alert('xss')</script>", id="xss-attempt"),
    pytest.param("../../../etc/passwd", id="path-traversal"),

    # Бульевы значения
    pytest.param("true", id="boolean_true"),
    pytest.param("false", id="boolean_false"),
    pytest.param("True", id="boolean_true_capitalized"),
    pytest.param("False", id="boolean_false_capitalized"),

    # Null/None
    pytest.param("null", id="null_value"),
    pytest.param("None", id="none_value"),

    # Массивы/Объекты (если API ожидает number)
    pytest.param("[123]", id="json_array"),
    pytest.param("{\"id\": 123}", id="json_object"),
]
