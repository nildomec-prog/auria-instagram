# AURIA · Publicación automática en Instagram (coste cero)

Este repositorio publica solo en @auria_solutions lo que pongas en `calendario.json`, a la hora que marques. Funciona con GitHub Actions y GitHub Pages, gratis en repositorios públicos, y con la API oficial de Instagram a través de una app de Meta tuya en modo desarrollo, que también es gratis y no necesita revisión de Meta porque solo accede a tu propia cuenta.

Qué hace:

- Publica carruseles, imágenes y reels en la fecha y hora del calendario (hora de Madrid) y guarda el enlace de cada publicación.
- Opcional: responde por mensaje privado a quien comente «12», «DEMO» o «DESPACHO».
- Renueva el token de Instagram los días 1 y 15 de cada mes, para que no caduque.

Octubre ya está cargado: 12 publicaciones del 5 al 30 de octubre, a las 13:30.

## Qué incluye

| Ruta | Para qué sirve |
| --- | --- |
| `calendario.json` | Qué se publica, cuándo y con qué texto. Aquí se guarda también el estado de cada publicación |
| `media/` | Las 55 imágenes JPEG (1080 × 1350) y los 6 reels animados en MP4 |
| `respuestas_dm.json` | Textos de los mensajes automáticos para «12», «DEMO» y «DESPACHO» |
| `scripts/` | Publicación, respuestas, validación y comprobación de la conexión |
| `.github/workflows/` | Las tareas programadas: publicar, renovar el token, validar y comprobar |

## Puesta en marcha: una sola vez, unos 30 minutos

### 1. Revisa la cuenta de Instagram

Tiene que ser profesional (ya lo es: empresa) y **pública**. Si fuera privada, Meta no genera el token.

### 2. Crea tu app de Meta

1. Entra en <https://developers.facebook.com/apps> y pulsa **Crear app**.
2. Nombre: `AURIA Publicador`. Correo: el tuyo.
3. Caso de uso: **Manage messaging & content on Instagram** (gestionar mensajes y contenido en Instagram). Si te pide tipo de app, **Business**.
4. Portfolio empresarial: **no conectar todavía**.
5. Pulsa **Crear app**. Déjala en **modo desarrollo**: no hace falta pasarla a producción ni pedir revisión.

### 3. Añade tu cuenta como evaluador

1. En la app: **Roles de la app → Roles → Añadir personas → Instagram Tester**. Escribe `auria_solutions` y pulsa **Añadir**.
2. En Instagram, con la cuenta de AURIA: **Configuración → Permisos de sitios web → Apps y sitios web → Invitaciones de evaluador** y acepta la invitación.

### 4. Genera el token

1. En la app: **Instagram → API setup with Instagram login → 1. Generate access tokens → Add account**, e inicia sesión con @auria_solutions.
2. Pulsa **Generate token** y acepta todos los permisos del aviso: publicar contenido y, si vas a activar las respuestas automáticas, comentarios y mensajes.
3. Copia el token y guárdalo en un sitio seguro: Meta solo lo enseña una vez. Dura 60 días y el repositorio lo renueva solo.

### 5. Crea el repositorio en GitHub

Crea un repositorio **público** llamado `auria-instagram` y sube todo el contenido de esta carpeta, incluida la carpeta oculta `.github`. Si prefieres hacerlo con Claude Code, tienes el prompt en `PROMPT_CLAUDE_CODE.md`.

Público significa que las imágenes y los textos se pueden ver antes de publicarse. No hay ninguna clave en el repositorio: los tokens van en secretos.

### 6. Activa GitHub Pages

**Settings → Pages → Source: Deploy from a branch → main / (root) → Save.** En uno o dos minutos tendrás la URL: `https://TU_USUARIO.github.io/auria-instagram`. De ahí descarga Instagram las imágenes y los vídeos.

### 7. Crea un token de GitHub para la renovación automática

En <https://github.com/settings/personal-access-tokens> → **Generate new token (fine-grained)**:

- Acceso solo a este repositorio (`auria-instagram`).
- Permiso: **Secrets → Read and write**.
- Caducidad: la máxima que permita (anótala en el calendario para renovarlo).

### 8. Guarda los secretos y las variables

**Settings → Secrets and variables → Actions.**

| Tipo | Nombre | Valor |
| --- | --- | --- |
| Secret | `IG_ACCESS_TOKEN` | El token de Instagram del paso 4 |
| Secret | `GH_PAT` | El token de GitHub del paso 7 |
| Variable | `MEDIA_BASE_URL` | La URL de Pages del paso 6, sin barra final |
| Variable (opcional) | `RESPUESTAS_ACTIVAS` | `true` cuando quieras activar los mensajes automáticos |
| Variable (opcional) | `IG_API_VERSION` | Por defecto `v25.0`. Cámbiala solo si Meta retira esa versión |

### 9. Comprueba que todo conecta

**Actions → Comprobar conexión → Run workflow.** Tiene que mostrar:

- `Token válido para @auria_solutions`;
- el cupo de publicación;
- `HTTP 200` para una imagen y un vídeo de `media/`.

### 10. Haz un ensayo

**Actions → Publicar en Instagram → Run workflow**, con «Solo simular» marcado y `C1` en «forzar_id». Te enseña las URLs que publicaría, sin publicar nada.

Listo. Desde aquí no tienes que hacer nada: cada 15 minutos se revisa el calendario y, cuando llega la hora, se publica. El enlace queda guardado en `calendario.json`.

## Calendario de octubre

| Fecha | Id | Tipo | Contenido |
| --- | --- | --- | --- |
| Lun 5 oct | C1 | Carrusel | Meses de caja |
| Mié 7 oct | A1 | Reel animado | ¿Llegas a Navidad? |
| Vie 9 oct | C2 | Imagen | El caso del 82 % |
| Mar 13 oct | C3 | Carrusel | Vendes más y ganas menos |
| Mié 14 oct | A2 | Reel animado | Tu empresa, con nota |
| Vie 16 oct | C4 | Carrusel | Para despachos |
| Lun 19 oct | C5 | Carrusel | Días de cobro |
| Mié 21 oct | V2 | Reel animado | El 82 % |
| Vie 23 oct | C6 | Carrusel | Así prioriza AURIA |
| Lun 26 oct | C7 | Carrusel | Punto de equilibrio |
| Mié 28 oct | A3 | Reel animado | Punto de equilibrio |
| Vie 30 oct | C8 | Carrusel | Autodiagnóstico en 12 preguntas |

Todas a las 13:30. Los reels grabados a cámara del plan original se han sustituido por reels animados, que no necesitan grabar a nadie. En `media/reels/` quedan además A4 (12 preguntas) y A5 (despachos) para noviembre.

## Añadir publicaciones

Añade una entrada a `calendario.json`, sube los archivos a `media/` y haz commit. Al subirlo se ejecuta la validación y, si algo no cumple, GitHub te avisa por email.

```json
{
  "id": "C9",
  "fecha": "2026-11-02",
  "hora": "13:30",
  "tipo": "CARRUSEL",
  "descripcion": "Carrusel: coste laboral",
  "archivos": ["media/C9/C9-01.jpg", "media/C9/C9-02.jpg"],
  "texto": "Texto del post...\n\n#pymes #controlling",
  "estado": "pendiente"
}
```

Reglas de la API de Instagram:

- Las imágenes deben ser **JPEG**, entre 4:5 y 1,91:1 (usa 1080 × 1350) y de menos de 8 MB.
- Un carrusel lleva de 2 a 10 imágenes.
- Un reel es un MP4 de 3 s a 15 min. `portada_ms` indica el milisegundo del vídeo que se usa como portada.
- Como máximo 5 hashtags por publicación.
- La hora es la de Madrid; el cambio de horario se aplica solo.

## Respuestas automáticas por DM (opcional)

Cada 15 minutos se revisan los comentarios de los últimos 7 días. A quien escriba «12», «DEMO» o «DESPACHO» se le envía una respuesta privada con el texto de `respuestas_dm.json`, una sola vez por comentario.

Para activarlas:

1. El token tiene que incluir los permisos de comentarios y mensajes (paso 4).
2. Crea la variable `RESPUESTAS_ACTIVAS` con el valor `true`.
3. Primero haz un ensayo con «Solo simular»: te lista a quién respondería.
4. Si Meta devuelve un error de permisos de mensajes, activa en la app de Instagram el acceso a mensajes para herramientas conectadas (Configuración → Mensajes y respuestas a historias → Controles de mensajes) y vuelve a generar el token.

Instagram solo permite una respuesta privada por comentario y dentro de los 7 días siguientes. Si la persona contesta, la conversación sigue en tu bandeja como cualquier otra.

## Si algo falla

- **Aviso por email.** GitHub te escribe cuando falla un paso. El motivo queda en el campo `error` de esa publicación en `calendario.json`.
- **Reintentos.** Se reintenta hasta 3 veces. Para volver a intentarlo, borra `intentos` y `error` o lánzalo a mano con `forzar_id`.
- **«The media could not be fetched».** Pages aún no ha desplegado los archivos o `MEDIA_BASE_URL` está mal escrita. Compruébalo con «Comprobar conexión».
- **Token caducado o inválido.** Repite el paso 4 y actualiza el secreto `IG_ACCESS_TOKEN`.
- **Retraso de más de 48 h.** La publicación se marca como `caducado` y no se publica tarde. Si aun así la quieres, cambia la fecha.
- **Inactividad.** GitHub desactiva las tareas programadas de un repositorio público tras 60 días sin actividad. Cada publicación deja un commit, así que mientras publiques no pasa.

## Lo que no se automatiza

- **Stories con encuesta, preguntas o enlace.** La API no permite stickers interactivos; súbelas desde la app, es un minuto.
- **Música de Instagram en los reels.** Los reels animados van sin música. Si quieres música, añádela antes con CapCut y sustituye el MP4.
- **Fijar publicaciones en el perfil.** Se hace desde la app.

## Plan B sin código

La app de Instagram y Meta Business Suite permiten programar publicaciones gratis. Sube las imágenes de `media/`, copia el texto de `calendario.json` y elige fecha y hora. Tendrás que hacerlo publicación a publicación.

## Coste

| Pieza | Coste |
| --- | --- |
| GitHub Actions (repositorio público) | 0 € |
| GitHub Pages (repositorio público) | 0 € |
| API de Instagram con app propia en modo desarrollo | 0 € |
| **Total** | **0 €** |
