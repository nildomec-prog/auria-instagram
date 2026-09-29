# Prompt para Claude Code

Descomprime `auria-instagram.zip`, abre Claude Code en esa carpeta (modelo Sonnet 4.6) y pega el prompt. Necesitas tener `gh` instalado y con la sesión iniciada (`gh auth login`).

```
Estás en la carpeta auria-instagram: una automatización de publicaciones de Instagram con GitHub Actions y GitHub Pages. Déjala publicada y configurada. No publiques nada en Instagram: cualquier ejecución del workflow de publicación tiene que ser en modo simulación.

1. Ejecuta python scripts/validar.py y confirma que termina sin errores (el aviso de fechas pasadas no bloquea).
2. Inicializa git en esta carpeta si no existe, con rama main, y crea con gh un repositorio PÚBLICO llamado auria-instagram en mi cuenta. Haz commit de todo, incluida la carpeta oculta .github, y push a main.
3. Activa GitHub Pages desde main y la carpeta raíz:
   gh api repos/{owner}/auria-instagram/pages -X POST -f "source[branch]=main" -f "source[path]=/"
4. Crea la variable del repositorio MEDIA_BASE_URL con la URL de Pages, sin barra final (https://<mi-usuario>.github.io/auria-instagram).
5. Espera a que Pages despliegue y comprueba con curl -I que devuelve 200 en MEDIA_BASE_URL/media/C1/C1-01.jpg y en MEDIA_BASE_URL/media/reels/A1_Navidad.mp4. Si aún da 404, espera un minuto y reintenta hasta 5 veces.
6. Los secretos los meto yo. Dime que ejecute en mi terminal estos dos comandos, que me pedirán el valor sin mostrarlo:
   gh secret set IG_ACCESS_TOKEN --repo <mi-usuario>/auria-instagram
   gh secret set GH_PAT --repo <mi-usuario>/auria-instagram
   Espera a que te confirme que están guardados. No me pidas que pegue los tokens en el chat.
7. Lanza el workflow "Comprobar conexión" con gh workflow run, espera a que termine y enséñame la salida.
8. Lanza el workflow "Publicar en Instagram" con modo_prueba=true y forzar_id=C1, espera a que termine y enséñame la salida.
9. Resume en 5 líneas: URL del repositorio, URL de Pages, resultado de la comprobación, resultado del ensayo y siguiente publicación programada.
```
