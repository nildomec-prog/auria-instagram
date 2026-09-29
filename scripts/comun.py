import os

import requests

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = os.environ.get("IG_API_VERSION") or "v25.0"
BASE = f"https://graph.instagram.com/{VERSION}"
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "")
MEDIA = (os.environ.get("MEDIA_BASE_URL") or "").rstrip("/")
PRUEBA = (os.environ.get("DRY_RUN") or "false").lower() == "true"


def limpiar(texto):
    return str(texto).replace(TOKEN, "***") if TOKEN else str(texto)


def api(metodo, ruta, json_body=None, **params):
    params["access_token"] = TOKEN
    url = f"{BASE}/{ruta}"
    if metodo == "GET":
        r = requests.get(url, params=params, timeout=60)
    elif json_body is not None:
        r = requests.post(url, params=params, json=json_body, timeout=120)
    else:
        r = requests.post(url, data=params, timeout=120)
    try:
        datos = r.json()
    except ValueError:
        datos = {"respuesta": r.text[:300]}
    if r.status_code >= 400 or "error" in datos:
        raise RuntimeError(limpiar(f"{metodo} {ruta} -> {datos}"))
    return datos


def usuario():
    elegido = (os.environ.get("IG_USER_ID") or "").strip()
    if elegido and elegido != "me":
        return elegido
    return str(api("GET", "me", fields="user_id")["user_id"])
