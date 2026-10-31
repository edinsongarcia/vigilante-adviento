"""Vigilante del calendario de adviento de Trendy (maquillajetrendyshop.com).
Revisa el catálogo (API pública de VTEX) una sola vez y avisa por Telegram
si hay un producto con la palabra clave y con stock. Sin dependencias externas.
"""
import json, os, sys, unicodedata, urllib.parse, urllib.request

BASE = "https://www.maquillajetrendyshop.com"
KEYWORD = os.environ.get("KEYWORD", "adviento").lower()
TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT = os.environ.get("TELEGRAM_CHAT_ID", "")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"


def norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def telegram(text):
    if not TOKEN or not CHAT:
        sys.exit("Faltan TELEGRAM_TOKEN o TELEGRAM_CHAT_ID")
    data = urllib.parse.urlencode({"chat_id": CHAT, "text": text}).encode()
    urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data, timeout=20)


def find_available():
    q = urllib.parse.quote(KEYWORD)
    url = f"{BASE}/api/catalog_system/pub/products/search?ft={q}&_from=0&_to=49"
    found = []
    for p in get_json(url):
        name = p.get("productName", "")
        if KEYWORD not in norm(name):
            continue
        for item in p.get("items", []):
            offers = [s.get("commertialOffer", {}) for s in item.get("sellers", [])]
            ok = [o for o in offers if o.get("IsAvailable") and o.get("AvailableQuantity", 0) > 0]
            if ok:
                found.append((name, p.get("link", BASE), ok[0].get("Price")))
                break
    return found


def set_output(value):
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a") as f:
            f.write(f"found={value}\n")


def main():
    if "--test" in sys.argv:
        telegram("✅ Prueba: el vigilante del calendario de adviento funciona.")
        print("Mensaje de prueba enviado.")
        return
    found = find_available()
    if not found:
        print("Aún no está disponible.")
        set_output("false")
        return
    for name, link, price in found:
        precio = f"${price:,.0f}" if price else ""
        telegram(f"🎄 ¡DISPONIBLE! {name} {precio}\n{link}")
        print("Aviso enviado:", name, link)
    set_output("true")


if __name__ == "__main__":
    main()
