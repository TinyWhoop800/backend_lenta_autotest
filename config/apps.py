from typing import Dict, List, Any

APPS_LENTA: List[Dict[str, Any]] = [
    {
        "app_name": "KinoLenta",
        "platform": "iOS",
        "headers": {
            'X-Device-ID': 'testb2cf59b36581399ebf54d4ab425ac4a1',
            'X-Locale': 'ru',
            'X-Client-App': 'tv.limehd.movie-reel'
        },
        "available_payment_methods": ["app store", "yookassa"],
        "payment_types": ["sbp", "bank_card", "sberbank", "tinkoff_bank"],
    },
    {
        "app_name": "KinoLenta",
        "platform": "Android",
        "headers": {
            'X-Device-ID': 'testb2cf59b36581399ebf54d4ab425ac4a1',
            'X-Locale': 'ru',
            'X-Client-App': 'reels.shorts.drama.kinolenta'
        },
        "available_payment_methods": ["yookassa"],
        "payment_types": ["sbp", "bank_card", "sberbank", "tinkoff_bank"],

    },
    {
        "app_name": "KinoLenta",
        "platform": "Web",
        "headers": {
            'X-Device-ID': 'testb2cf59b36581399ebf54d4ab425ac4a1',
            'X-Locale': 'ru',
            'X-Client-App': 'kino-lenta.ru'
        }
    },
    {
        "app_name": "ReelPix",
        "platform": "iOS",
        "headers": {
            'X-Device-ID': 'testb2cf59b36581399ebf54d4ab425ac4a1',
            'X-Locale': 'en',
            'X-Client-App': 'shorts.drama.reelpix'
        },
        "available_payment_methods": ["app store"]
    },
    {
        "app_name": "ReelPix",
        "platform": "Web",
        "headers": {
            'X-Device-ID': 'testb2cf59b36581399ebf54d4ab425ac4a1',
            'X-Locale': 'en',
            'X-Client-App': 'reelpix.show'
        }
    },
    {
        "app_name": "ReelPix",
        "platform": "Android",
        "headers": {
            'X-Device-ID': 'testb2cf59b36581399ebf54d4ab425ac4a1',
            'X-Locale': 'en',
            'X-Client-App': 'com.shorts.drama.reelpix'
        },
        "available_payment_methods": ["google play"]
    },
    {
        "app_name": "RJOY",
        "platform": "iOS",
        "headers": {
            'X-Device-ID': 'testb2cf59b36581399ebf54d4ab425ac4a1',
            'X-Locale': 'en',
            'X-Client-App': 'rjoy.reel.short.drama'
        },
        "available_payment_methods": ["app store"]
    },
    {
        "app_name": "RJOY",
        "platform": "Android",
        "headers": {
            'X-Device-ID': 'testb2cf59b36581399ebf54d4ab425ac4a1',
            'X-Locale': 'en',
            'X-Client-App': 'rjoy.story.shorts.drama'
        },
        "available_payment_methods": ["google play"]
    },
]
