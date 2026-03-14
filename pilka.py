import asyncio
import json
import os
import time
import requests
from datetime import datetime, timezone

FDORG_KEY    = "9392466449464e0aa99d278b86192401"
FDORG_URL    = "https://api.football-data.org/v4"
PILKA_PLIK   = "pilka.json"
REFRESH_SECS = 12 * 3600
RATE_DELAY   = 7


HEADERS = {"X-Auth-Token": FDORG_KEY}

LIGI = {
    "CL":  "UEFA Champions League",
    "FL1": "Ligue 1",
    "PL":  "Premier League",
    "BL1": "Bundesliga",
    "SA":  "Serie A",
    "PD":  "La Liga",
}

PSG_ID = 524

def _get(endpoint: str, params: dict = {}) -> dict:
    for attempt in range(3):
        resp = requests.get(f"{FDORG_URL}/{endpoint}", headers=HEADERS, params=params, timeout=30)
        if resp.status_code == 429:
            print(f"[pilka] rate limit, czekam 65s...")
            time.sleep(65)
            continue
        resp.raise_for_status()
        return resp.json()
    return {}

def _fetch_standings(code: str) -> list[dict]:
    try:
        data = _get(f"competitions/{code}/standings")
        tabela = data["standings"][0]["table"]
        return [
            {
                "miejsce": t["position"],
                "druzyna": t["team"]["name"],
                "pkt":     t["points"],
                "m":       t["playedGames"],
                "gole":    f"{t['goalsFor']}:{t['goalsAgainst']}",
            }
            for t in tabela[:10]
        ]
    except Exception as e:
        print(f"[pilka] standings {code}: {e}")
        return []

def _fetch_matches(code: str, status: str, limit: int = 5) -> list[dict]:
    try:
        data = _get(f"competitions/{code}/matches", {"status": status, "limit": limit})
        wyniki = []
        for m in data.get("matches", [])[:limit]:
            home  = m["homeTeam"]["name"] or "?"
            away  = m["awayTeam"]["name"] or "?"
            score = m.get("score", {})
            full  = score.get("fullTime", {})
            gh    = full.get("home")
            ga    = full.get("away")
            wynik = f"{gh}:{ga}" if gh is not None else "—"
            wyniki.append({
                "data":   (m.get("utcDate") or "")[:10],
                "mecz":   f"{home} vs {away}",
                "wynik":  wynik,
                "status": m.get("status", "?"),
            })
        return wyniki
    except Exception as e:
        print(f"[pilka] matches {code} {status}: {e}")
        return []

def _fetch_scorers(code: str, limit: int = 8) -> list[dict]:
    try:
        data = _get(f"competitions/{code}/scorers", {"limit": limit})
        return [
            {
                "imie":    s["player"]["name"],
                "druzyna": s["team"]["name"],
                "gole":    s.get("goals", 0),
                "asysty":  s.get("assists", 0) or 0,
            }
            for s in data.get("scorers", [])
        ]
    except Exception as e:
        print(f"[pilka] scorers {code}: {e}")
        return []

def _fetch_psg_matches() -> list[dict]:
    try:
        data = _get(f"teams/{PSG_ID}/matches", {"limit": 10})
        wyniki = []
        for m in data.get("matches", []):
            home  = m["homeTeam"]["name"] or "?"
            away  = m["awayTeam"]["name"] or "?"
            score = m.get("score", {})
            full  = score.get("fullTime", {})
            gh    = full.get("home")
            ga    = full.get("away")
            wynik = f"{gh}:{ga}" if gh is not None else "—"
            wyniki.append({
                "data":   (m.get("utcDate") or "")[:10],
                "mecz":   f"{home} vs {away}",
                "wynik":  wynik,
                "liga":   m.get("competition", {}).get("name", "?"),
                "status": m.get("status", "?"),
            })
        wyniki.sort(key=lambda x: x["data"], reverse=True)
        return wyniki[:10]
    except Exception as e:
        print(f"[pilka] psg matches: {e}")
        return []


def _fetch_psg_squad() -> list[dict]:
    try:
        data = _get(f"teams/{PSG_ID}")
        squad = data.get("squad", [])
        gracze = []
        for p in squad:
            gracze.append({
                "imie":     p.get("name", "?"),
                "pozycja":  p.get("position", "?"),
                "numer":    p.get("shirtNumber", "?"),
                "narodowosc": p.get("nationality", "?"),
                "wiek":     p.get("dateOfBirth", "?")[:4] if p.get("dateOfBirth") else "?",
            })
        pozycje = {"Goalkeeper": "Bramkarz", "Defence": "Obronca", "Midfield": "Pomocnik", "Offence": "Napastnik"}
        gracze.sort(key=lambda x: list(pozycje.keys()).index(x["pozycja"]) if x["pozycja"] in pozycje else 99)
        return gracze
    except Exception as e:
        print(f"[pilka] psg squad: {e}")
        return []

def wczytaj_pilke() -> dict:
    if os.path.exists(PILKA_PLIK):
        try:
            with open(PILKA_PLIK, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def zapisz_pilke(dane: dict):
    with open(PILKA_PLIK, "w", encoding="utf-8") as f:
        json.dump(dane, f, ensure_ascii=False, indent=2)

def odswiez_dane_pilkarskie():
    if os.path.exists(PILKA_PLIK):
        os.remove(PILKA_PLIK)

    print("odswieżanie info o pilce...")
    dane = {
        "ostatni_update": datetime.now(timezone.utc).isoformat(),
        "mecze_psg":      _fetch_psg_matches(),
        "sklad_psg":      _fetch_psg_squad(),
        "tabele":         {},
        "ostatnie_mecze": {},
        "nadchodzace":    {},
        "strzelcy":       {},
    }

    time.sleep(RATE_DELAY)
    for code in LIGI:
        time.sleep(RATE_DELAY)
        dane["tabele"][code] = _fetch_standings(code)
        time.sleep(RATE_DELAY)
        dane["ostatnie_mecze"][code] = _fetch_matches(code, "FINISHED", 5)
        time.sleep(RATE_DELAY)
        dane["nadchodzace"][code] = _fetch_matches(code, "SCHEDULED", 5)
        time.sleep(RATE_DELAY)
        dane["strzelcy"][code] = _fetch_scorers(code, 8)
        print(f"[pilka] {code} gotowe")

    zapisz_pilke(dane)
    print("[pilka] wszystko zapisane")
    return dane

def pilka_jako_tekst() -> str:
    dane = wczytaj_pilke()
    if not dane:
        return "(brak danych pilkarskich)"

    czesci = []
    update = dane.get("ostatni_update", "?")[:16].replace("T", " ")
    czesci.append(f"DANE PILKARSKIE (update: {update} UTC):")

    mecze_psg = dane.get("mecze_psg", [])
    if mecze_psg:
        czesci.append("\nMecze PSG (wszystkie rozgrywki):")
        for m in mecze_psg:
            czesci.append(f"  {m['data']} | {m['mecz']} | {m['wynik']} | {m['liga']} [{m['status']}]")

    sklad = dane.get("sklad_psg", [])
    if sklad:
        pozycje_pl = {"Goalkeeper": "Bramkarz", "Defence": "Obronca", "Midfield": "Pomocnik", "Offence": "Napastnik"}
        czesci.append("\nSklad PSG:")
        for p in sklad:
            poz = pozycje_pl.get(p["pozycja"], p["pozycja"])
            czesci.append(f"  #{p['numer']} {p['imie']} | {poz} | {p['narodowosc']} | ur. {p['wiek']}")

    for code, nazwa in LIGI.items():
        tabela      = dane.get("tabele", {}).get(code, [])
        ostatnie    = dane.get("ostatnie_mecze", {}).get(code, [])
        nadchodzace = dane.get("nadchodzace", {}).get(code, [])
        strzelcy    = dane.get("strzelcy", {}).get(code, [])

        czesci.append(f"\n=== {nazwa} ===")

        if tabela:
            czesci.append("Tabela (top 10):")
            for t in tabela:
                psg = " <- PSG" if "Paris" in t["druzyna"] else ""
                czesci.append(f"  {t['miejsce']}. {t['druzyna']} {t['pkt']}pkt ({t['m']}m, {t['gole']}){psg}")

        if ostatnie:
            czesci.append("Ostatnie wyniki:")
            for m in ostatnie:
                czesci.append(f"  {m['data']} | {m['mecz']} | {m['wynik']}")

        if nadchodzace:
            czesci.append("Nadchodzace mecze:")
            for m in nadchodzace:
                czesci.append(f"  {m['data']} | {m['mecz']}")

        if strzelcy:
            czesci.append("Krolowie strzelcow:")
            for s in strzelcy:
                czesci.append(f"  {s['imie']} ({s['druzyna']}): {s['gole']}g {s['asysty']}a")

    return "\n".join(czesci)

async def task_pilka():
    await asyncio.sleep(5)
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, odswiez_dane_pilkarskie)
    except Exception as e:
        print(f"[task_pilka] start: {e}")
    while True:
        await asyncio.sleep(REFRESH_SECS)
        try:
            await loop.run_in_executor(None, odswiez_dane_pilkarskie)
        except Exception as e:
            print(f"[task_pilka] refresh: {e}")