#!/usr/bin/env python3
"""Comprueba el calendario y los archivos antes de que se publiquen."""
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    errores, avisos, ids = [], [], set()
    cal = json.load(open(os.path.join(RAIZ, "calendario.json"), encoding="utf-8"))
    zona = ZoneInfo(cal.get("zona_horaria", "Europe/Madrid"))
    ahora = dt.datetime.now(zona)
    for p in cal.get("publicaciones", []):
        pid = p.get("id", "?")
        if pid in ids:
            errores.append(f"{pid}: id repetido")
        ids.add(pid)
        falta = [k for k in ("fecha", "hora", "tipo", "archivos", "texto") if k not in p]
        if falta:
            errores.append(f"{pid}: faltan campos {falta}")
            continue
        if p["tipo"] not in ("IMAGEN", "CARRUSEL", "REEL"):
            errores.append(f"{pid}: tipo {p['tipo']} no válido (IMAGEN, CARRUSEL o REEL)")
        try:
            cuando = dt.datetime.fromisoformat(f"{p['fecha']}T{p['hora']}").replace(tzinfo=zona)
            if p.get("estado", "pendiente") == "pendiente" and cuando < ahora:
                avisos.append(f"{pid}: la fecha ya pasó y sigue pendiente")
        except ValueError:
            errores.append(f"{pid}: fecha u hora mal escritas (AAAA-MM-DD y HH:MM)")
        if len(p["texto"]) > 2200:
            errores.append(f"{pid}: el texto supera 2.200 caracteres")
        if len(re.findall(r"#\w+", p["texto"])) > 5:
            errores.append(f"{pid}: más de 5 hashtags (Instagram solo admite 5)")
        arch = p["archivos"]
        if p["tipo"] == "CARRUSEL" and not 2 <= len(arch) <= 10:
            errores.append(f"{pid}: un carrusel necesita de 2 a 10 imágenes")
        if p["tipo"] in ("IMAGEN", "REEL") and len(arch) != 1:
            errores.append(f"{pid}: {p['tipo']} lleva un solo archivo")
        for a in arch:
            ruta = os.path.join(RAIZ, a)
            if not os.path.exists(ruta):
                errores.append(f"{pid}: no existe {a}")
                continue
            if p["tipo"] in ("IMAGEN", "CARRUSEL"):
                with Image.open(ruta) as im:
                    if im.format != "JPEG":
                        errores.append(f"{pid}: {a} debe ser JPEG (la API de Instagram solo acepta JPEG)")
                    ancho, alto = im.size
                    if not 0.79 <= ancho / alto <= 1.92:
                        errores.append(f"{pid}: {a} mide {ancho}x{alto}; la proporción debe ir de 4:5 a 1,91:1")
                if os.path.getsize(ruta) > 8 * 1024 * 1024:
                    errores.append(f"{pid}: {a} pesa más de 8 MB")
            else:
                if not a.lower().endswith((".mp4", ".mov")):
                    errores.append(f"{pid}: {a} debe ser MP4 o MOV")
                if shutil.which("ffprobe"):
                    salida = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                             "csv=p=0", ruta], capture_output=True, text=True).stdout.strip()
                    if salida and not 3 <= float(salida) <= 900:
                        errores.append(f"{pid}: el vídeo dura {float(salida):.0f} s; debe durar de 3 s a 15 min")
    for a in avisos:
        print(f"Aviso: {a}")
    for e in errores:
        print(f"ERROR: {e}")
    print(f"{len(cal.get('publicaciones', []))} publicaciones revisadas, {len(errores)} errores.")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
