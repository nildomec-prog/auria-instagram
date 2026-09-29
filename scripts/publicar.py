#!/usr/bin/env python3
"""Publica en Instagram lo que toca según calendario.json. Una publicación por ejecución."""
import datetime as dt
import json
import os
import sys
import time
from zoneinfo import ZoneInfo

from comun import MEDIA, PRUEBA, RAIZ, TOKEN, api, limpiar, usuario

CALENDARIO = os.path.join(RAIZ, "calendario.json")
FORZAR = (os.environ.get("FORCE_ID") or "").strip()
MAX_INTENTOS = 3
CADUCIDAD = dt.timedelta(hours=48)


def esperar(contenedor, limite):
    inicio = time.time()
    while time.time() - inicio < limite:
        estado = api("GET", contenedor, fields="status_code").get("status_code")
        if estado == "FINISHED":
            return
        if estado in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"El contenedor {contenedor} quedó en estado {estado}")
        time.sleep(5)
    raise RuntimeError(f"El contenedor {contenedor} no terminó de procesarse en {limite} s")


def url(ruta):
    return f"{MEDIA}/{ruta}"


def ya_publicada(uid, pub):
    inicio = pub["texto"][:80]
    for m in api("GET", f"{uid}/media", fields="id,caption,permalink", limit="10").get("data", []):
        if (m.get("caption") or "").startswith(inicio):
            return m
    return None


def publicar(uid, pub):
    tipo, texto, archivos = pub["tipo"], pub["texto"], pub["archivos"]
    if tipo == "IMAGEN":
        contenedor = api("POST", f"{uid}/media", image_url=url(archivos[0]), caption=texto)["id"]
        esperar(contenedor, 300)
    elif tipo == "CARRUSEL":
        hijos = [api("POST", f"{uid}/media", image_url=url(a), is_carousel_item="true")["id"] for a in archivos]
        for h in hijos:
            esperar(h, 300)
        contenedor = api("POST", f"{uid}/media", media_type="CAROUSEL", children=",".join(hijos), caption=texto)["id"]
        esperar(contenedor, 300)
    elif tipo == "REEL":
        extra = {}
        if pub.get("portada_ms") is not None:
            extra["thumb_offset"] = str(pub["portada_ms"])
        contenedor = api("POST", f"{uid}/media", media_type="REELS", video_url=url(archivos[0]), caption=texto,
                         share_to_feed="true", **extra)["id"]
        esperar(contenedor, 900)
    else:
        raise RuntimeError(f"Tipo desconocido: {tipo}")
    media_id = api("POST", f"{uid}/media_publish", creation_id=contenedor)["id"]
    return media_id, api("GET", media_id, fields="permalink").get("permalink")


def main():
    with open(CALENDARIO, encoding="utf-8") as f:
        cal = json.load(f)
    zona = ZoneInfo(cal.get("zona_horaria", "Europe/Madrid"))
    ahora = dt.datetime.now(zona)
    cambios, fallo, hecho = False, False, False
    for pub in cal["publicaciones"]:
        if pub.get("estado") in ("publicado", "omitido", "caducado"):
            continue
        if FORZAR and pub["id"] != FORZAR:
            continue
        cuando = dt.datetime.fromisoformat(f"{pub['fecha']}T{pub['hora']}").replace(tzinfo=zona)
        if not FORZAR:
            if cuando > ahora:
                continue
            if ahora - cuando > CADUCIDAD:
                print(f"{pub['id']}: más de 48 h de retraso; se marca como caducada y no se publica.")
                pub["estado"] = "caducado"
                cambios = True
                continue
            if pub.get("intentos", 0) >= MAX_INTENTOS:
                continue
        print(f"{pub['id']} ({pub['tipo']}), programada para el {cuando:%d/%m/%Y a las %H:%M}")
        hecho = True
        if PRUEBA:
            print("  Modo prueba. Se publicaría con estos archivos:")
            for a in pub["archivos"]:
                print(f"   - {url(a) if MEDIA else a}")
            break
        if not TOKEN or not MEDIA:
            sys.exit("Hay una publicación pendiente pero faltan IG_ACCESS_TOKEN o MEDIA_BASE_URL: "
                     "revisa los secretos y variables del repositorio.")
        try:
            uid = usuario()
            previa = ya_publicada(uid, pub)
            if previa:
                media_id, enlace = previa["id"], previa.get("permalink")
                print("  Ya estaba publicada: solo actualizo el estado.")
            else:
                media_id, enlace = publicar(uid, pub)
            pub.update(estado="publicado", media_id=media_id, enlace=enlace,
                       publicado_en=dt.datetime.now(zona).isoformat(timespec="seconds"))
            pub.pop("error", None)
            print(f"  Publicada: {enlace}")
        except Exception as e:
            pub["intentos"] = pub.get("intentos", 0) + 1
            pub["error"] = limpiar(e)[:600]
            print(f"  ERROR (intento {pub['intentos']} de {MAX_INTENTOS}): {pub['error']}")
            fallo = True
        cambios = True
        break
    if not hecho:
        print("Nada que publicar ahora.")
    if cambios and not PRUEBA:
        with open(CALENDARIO, "w", encoding="utf-8") as f:
            json.dump(cal, f, ensure_ascii=False, indent=2)
            f.write("\n")
    if fallo:
        sys.exit(1)


if __name__ == "__main__":
    main()
