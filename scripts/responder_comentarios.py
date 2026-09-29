#!/usr/bin/env python3
"""Responde por mensaje privado a los comentarios con palabra clave (12, DEMO, DESPACHO)."""
import datetime as dt
import json
import os
import re
import sys

from comun import PRUEBA, RAIZ, TOKEN, api, limpiar, usuario

ESTADO = os.path.join(RAIZ, "respuestas.json")
PLANTILLAS = os.path.join(RAIZ, "respuestas_dm.json")
ACTIVAS = (os.environ.get("RESPUESTAS_ACTIVAS") or "false").lower() == "true"


def fecha(ts):
    return dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z")


def main():
    if not ACTIVAS and not PRUEBA:
        print("Respuestas automáticas desactivadas (variable RESPUESTAS_ACTIVAS).")
        return
    if not TOKEN:
        print("Sin IG_ACCESS_TOKEN: no reviso comentarios.")
        return
    reglas = json.load(open(PLANTILLAS, encoding="utf-8"))["reglas"]
    estado = json.load(open(ESTADO, encoding="utf-8")) if os.path.exists(ESTADO) else {"respondidos": []}
    hechos = set(estado.get("respondidos", []))
    uid = usuario()
    yo = api("GET", "me", fields="username").get("username")
    limite = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7)
    enviados, fallos = 0, 0
    for m in api("GET", f"{uid}/media", fields="id,timestamp", limit="15").get("data", []):
        if fecha(m["timestamp"]) < limite:
            continue
        for c in api("GET", f"{m['id']}/comments", fields="id,text,username,timestamp", limit="50").get("data", []):
            if c["id"] in hechos or c.get("username") == yo or fecha(c["timestamp"]) < limite:
                continue
            texto = (c.get("text") or "").lower()
            regla = next((r for r in reglas if re.search(r["patron"], texto)), None)
            if not regla:
                continue
            print(f"@{c.get('username')} comentó «{texto[:40]}» -> respuesta {regla['clave']}")
            if PRUEBA:
                continue
            try:
                api("POST", f"{uid}/messages",
                    json_body={"recipient": {"comment_id": c["id"]}, "message": {"text": regla["texto"]}})
                hechos.add(c["id"])
                enviados += 1
            except Exception as e:
                print(f"  ERROR: {limpiar(e)}")
                fallos += 1
    if not PRUEBA:
        estado["respondidos"] = sorted(hechos)[-3000:]
        with open(ESTADO, "w", encoding="utf-8") as f:
            json.dump(estado, f, indent=2)
            f.write("\n")
    print(f"Mensajes enviados: {enviados}")
    if fallos:
        sys.exit(1)


if __name__ == "__main__":
    main()
