# Vigilante calendario de adviento Trendy

## 1. Crear el bot de Telegram
1. En Telegram abre **@BotFather** → `/newbot` → guarda el **token**.
2. Abre tu bot nuevo y envíale cualquier mensaje.
3. En el navegador abre `https://api.telegram.org/bot<TOKEN>/getUpdates`
   y copia el número de `"chat":{"id": ...}` → ese es tu **chat id**.

## 2. Subir a GitHub
1. Crea un repositorio nuevo (público = minutos ilimitados).
2. Sube `check.py` y `.github/workflows/vigilante.yml` (respeta esa ruta).
3. Settings → Secrets and variables → Actions → New repository secret:
   - `TELEGRAM_TOKEN`
   - `TELEGRAM_CHAT_ID`
   (No pongas el token en el código, y menos en un repo público.)

## 3. Probar
Pestaña **Actions** → "Vigilante calendario" → Run workflow → marca *test*.
Debe llegarte un mensaje. Luego córrelo sin *test* para verificar que no da error.

## Notas
- Corre cada ~5 min (GitHub puede retrasarlo).
- Al avisar, se desactiva solo. Para reanudar: Actions → Enable workflow.
- Para vigilar otra palabra, agrega la variable `KEYWORD` en el workflow.
- Si el workflow falla (ej. la API bloquea las IP de GitHub), te llegará un correo de GitHub.
