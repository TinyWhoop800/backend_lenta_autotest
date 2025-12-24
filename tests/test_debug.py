import requests

def test_direct_request():
    """Прямой запрос без ваших классов"""
    url = "https://lenta-test.iptv2021.com/api/v1/login/guest"
    headers = {
        'X-Device-ID': 'testb2cf59b36581399ebf54d4ab425ac4a1',
        'X-Locale': 'ru',
        'X-Client-App': 'tv.limehd.movie-reel'
    }

    print(f"URL: {url}")
    print(f"Headers: {headers}")

    response = requests.post(url, headers=headers)

    print(f"Status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Response body: {response.text[:500]}")

    # Если есть редирект
    if response.history:
        print(f"Redirected from: {response.history[0].url}")