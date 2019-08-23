import requests
from bs4 import BeautifulSoup
import os

def get_text_for_lawsuit(court_id, lawsuit_id, lawsuit_password):
    soup = fetch_lawsuit_data(
        court_id=court_id,
        lawsuit_id=lawsuit_id,
        lawsuit_password=lawsuit_password,
    )

    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    text = '\n'.join(line for line in lines if line)

    return text

def fetch_lawsuit_data(court_id, lawsuit_id, lawsuit_password):

    HEADERS_COMMON = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
        "Connection": "keep-alive",
        "Host": "sagace.juradm.fr",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.99 Chrome/67.0.3396.99 Safari/537.36",
    }

    def send_request_1():
        headers = HEADERS_COMMON

        response = requests.get(
            'https://sagace.juradm.fr/Authentification.aspx',
            headers=headers,
            allow_redirects=False,
        )

        assert response.status_code == 302

        asp_net_session_id = response.headers['Set-Cookie'].split(';')[0]
        assert 'persist=401v-80' in response.headers['Set-Cookie']
        cookie = '{}; persist=401v-80'.format(asp_net_session_id)

        return cookie

    def send_request_2(cookie):
        headers = {
            **HEADERS_COMMON,
            'Cookie': cookie,
        }

        response = requests.get(
            'https://sagace.juradm.fr/Cook.aspx',
            headers=headers,
            allow_redirects=False,
        )
        assert response.status_code == 302

    def send_request_3(cookie):
        headers = {
            **HEADERS_COMMON,
            'Cookie': cookie,
        }

        response = requests.get(
            'https://sagace.juradm.fr/Authentification.aspx',
            headers=headers,
            allow_redirects=False,
        )
        assert response.status_code == 200

    def send_request_4(cookie, court_id, lawsuit_id, lawsuit_password):
        headers = {
            **HEADERS_COMMON,
            'Cookie': cookie,
            'Cache-Control': 'max-age=0',
            'Content-Length': '504',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://sagace.juradm.fr',
            'Referer': 'https://sagace.juradm.fr/Authentification.aspx',
        }

        data = {
            '__VIEWSTATE': '/wEPDwULLTE1NTE4NDkxNjQPZBYCAgEPZBYCAgMPD2QWAh4Hb25jbGljawUgQWN0aW9uKCk7X19kb1Bvc3RCYWNrKCdpYk9rJywnJylkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQRpYk9rqXmtB12mj9uUmm9kmptVyycImvikhFb10CfysBTnnKM=',
            '__VIEWSTATEGENERATOR': '485AC012',
            '__EVENTVALIDATION': '/wEdAAXSLsuptIuswQrdCTNuahyRg9RxSu3Vu7cDsvIlWIG+dRBAkDdsywjS0YnNj8VOZ9KTCd0U23v3NFv3G1TRsBun6096EZxc6ElGtLBK29KEGz3NxF3lB5oLioGvqq74fZ0nogrDIKt0MFfg3fEahdVs',
            'TxtJuridiction': court_id,
            'TxtDossier': lawsuit_id,
            'TxtAleaCle': lawsuit_password,
            'ibOk.x': '60',
            'ibOk.y': '13',
        }

        response = requests.post(
            'https://sagace.juradm.fr/Authentification.aspx',
            headers=headers,
            data=data,
            allow_redirects=False,
        )
        assert response.status_code == 302

    def send_request_5(cookie):
        headers = {
            **HEADERS_COMMON,
            'Cookie': cookie,
            'Cache-Control': 'max-age=0',
            'Referer': 'https://sagace.juradm.fr/Authentification.aspx',
        }

        response = requests.get(
            'https://sagace.juradm.fr/Dossier.aspx',
            headers=headers,
            allow_redirects=False,
        )
        assert response.status_code == 200

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    cookie = send_request_1()
    send_request_2(cookie=cookie)
    send_request_3(cookie=cookie)
    send_request_4(
        cookie=cookie,
        court_id=court_id,
        lawsuit_id=lawsuit_id,
        lawsuit_password=lawsuit_password,
    )
    soup = send_request_5(cookie=cookie)
    
    return soup
