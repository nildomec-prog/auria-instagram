#!/usr/bin/env python3
"""Comprueba el token, la cuenta y que los archivos se pueden descargar desde la URL pública."""
import json
import os
import sys

import requests

from comun import MEDIA, RAIZ, TOKEN, api, limpiar


def main():
    ok = True
    try:
        yo = api("GET", "me", fields="user_id,username,account_type")
        print(f"Token válido para @{yo.get('username')} ({yo.get('account_type')}), user_id {yo.get('user_id')}")
        cupo = api("GET", f"{yo['user_id']}/content_publishing_limit", fields="quota_usage,config")
        print("Cupo de publicación:", json.dumps(cupo.get("data", cupo), ensure_ascii=False))
    except Exception as e:
        print(f"Token o cuenta: ERROR -> {limpiar(e)}")
        ok = False
    cal = json.load(open(os.path.join(RAIZ, "calendario.json"), encoding="utf-8"))
    for ruta in (cal["publicaciones"][0]["archivos"][0], "media/reels/A1_Navidad.mp4"):
        url = f"{MEDIA}/{ruta}"
        try:
            r = requests.head(url, timeout=30, allow_redirects=True)
            print(f"{url} -> HTTP {r.status_code}, {r.headers.get('content-type')}")
            ok = ok and r.status_code == 200
        except Exception as e:
            print(f"{url} -> ERROR {e}")
            ok = False
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
