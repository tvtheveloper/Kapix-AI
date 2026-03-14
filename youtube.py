import asyncio
import json
import os
import requests
from datetime import datetime, timezone

YT_API_KEY   = "AIzaSyADo4NLqV7olIEXbIbH791cKLIfUrbu3ms"
YT_API_URL   = "https://www.googleapis.com/youtube/v3"
YT_PLIK      = "youtube.json"
REFRESH_SECS = 12 * 3600

BIRUTEQQ_HANDLE = "Biruteqq"

BIRUTEQQ_INFO = """Biruteqq (znany jako "birut") — wlasciciel i twarz "Strefy Kart", popularnego kanalu/projektu zwiazanego z kartami kolekcjonerskimi (glownie FIFA/FC i podobne). Prowadzi kanal na YouTube gdzie wrzuca filmy zwiazane z kartami, otwieraniem paczek i tematami zwiazanymi z Warstwa Kart. Znana postac w polskiej spolecznosci kart."""

def _get_channel_id(handle: str) -> str | None:
    try:
        resp = requests.get(f"{YT_API_URL}/channels", params={
            "part":      "id",
            "forHandle": handle.lstrip("@"),
            "key":       YT_API_KEY,
        }, timeout=30)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return items[0]["id"] if items else None
    except Exception as e:
        print(f"[youtube] get_channel_id: {e}")
        return None

def _get_channel_stats(channel_id: str) -> dict:
    try:
        resp = requests.get(f"{YT_API_URL}/channels", params={
            "part": "snippet,statistics,brandingSettings,contentDetails",
            "id":   channel_id,
            "key":  YT_API_KEY,
        }, timeout=30)
        resp.raise_for_status()
        item  = resp.json()["items"][0]
        snip  = item["snippet"]
        stats = item["statistics"]
        return {
            "nazwa":             snip.get("title", "?"),
            "opis":              snip.get("description", "")[:400],
            "kraj":              snip.get("country", "?"),
            "zalozony":          snip.get("publishedAt", "?")[:10],
            "subskrypcje":       stats.get("subscriberCount", "ukryte"),
            "filmy_total":       stats.get("videoCount", "?"),
            "wyswietlen_lacznie": stats.get("viewCount", "?"),
            "uploads_playlist":  item.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads", ""),
        }
    except Exception as e:
        print(f"[youtube] get_channel_stats: {e}")
        return {}

def _get_video_stats(video_ids: list[str]) -> dict:
    try:
        resp = requests.get(f"{YT_API_URL}/videos", params={
            "part": "statistics,contentDetails",
            "id":   ",".join(video_ids),
            "key":  YT_API_KEY,
        }, timeout=30)
        resp.raise_for_status()
        wynik = {}
        for item in resp.json().get("items", []):
            stats = item.get("statistics", {})
            dur   = item.get("contentDetails", {}).get("duration", "?")
            wynik[item["id"]] = {
                "wyswietlen": stats.get("viewCount", "0"),
                "lajki":      stats.get("likeCount", "0"),
                "komentarze": stats.get("commentCount", "0"),
                "dlugosc":    dur,
            }
        return wynik
    except Exception as e:
        print(f"[youtube] get_video_stats: {e}")
        return {}

def _get_last_videos(uploads_playlist_id: str, limit: int = 15) -> list[dict]:
    try:
        resp = requests.get(f"{YT_API_URL}/playlistItems", params={
            "part":       "snippet,contentDetails",
            "playlistId": uploads_playlist_id,
            "maxResults": limit,
            "key":        YT_API_KEY,
        }, timeout=30)
        resp.raise_for_status()
        filmy = []
        for item in resp.json().get("items", []):
            snip = item["snippet"]
            filmy.append({
                "tytul":    snip.get("title", "?"),
                "data":     snip.get("publishedAt", "?")[:10],
                "video_id": snip.get("resourceId", {}).get("videoId", ""),
                "opis":     snip.get("description", "")[:200],
            })
        if filmy:
            ids       = [f["video_id"] for f in filmy if f["video_id"]]
            stats_map = _get_video_stats(ids)
            for f in filmy:
                s = stats_map.get(f["video_id"], {})
                f["wyswietlen"] = s.get("wyswietlen", "?")
                f["lajki"]      = s.get("lajki", "?")
                f["komentarze"] = s.get("komentarze", "?")
                f["dlugosc"]    = s.get("dlugosc", "?")
        return filmy
    except Exception as e:
        print(f"[youtube] get_last_videos: {e}")
        return []

def _get_top_videos(channel_id: str, limit: int = 10) -> list[dict]:
    try:
        resp = requests.get(f"{YT_API_URL}/search", params={
            "part":       "snippet",
            "channelId":  channel_id,
            "order":      "viewCount",
            "type":       "video",
            "maxResults": limit,
            "key":        YT_API_KEY,
        }, timeout=30)
        resp.raise_for_status()
        filmy = []
        for item in resp.json().get("items", []):
            snip = item["snippet"]
            filmy.append({
                "tytul":    snip.get("title", "?"),
                "data":     snip.get("publishedAt", "?")[:10],
                "video_id": item["id"].get("videoId", ""),
            })
        if filmy:
            ids       = [f["video_id"] for f in filmy if f["video_id"]]
            stats_map = _get_video_stats(ids)
            for f in filmy:
                s = stats_map.get(f["video_id"], {})
                f["wyswietlen"] = s.get("wyswietlen", "?")
                f["lajki"]      = s.get("lajki", "?")
        return filmy
    except Exception as e:
        print(f"[youtube] get_top_videos: {e}")
        return []

def wczytaj_yt() -> dict:
    if os.path.exists(YT_PLIK):
        try:
            with open(YT_PLIK, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def zapisz_yt(dane: dict):
    with open(YT_PLIK, "w", encoding="utf-8") as f:
        json.dump(dane, f, ensure_ascii=False, indent=2)

def odswiez_dane_youtube():
    if os.path.exists(YT_PLIK):
        os.remove(YT_PLIK)

    print("[youtube] odswiezam...")

    channel_id = _get_channel_id(BIRUTEQQ_HANDLE)
    if not channel_id:
        print("[youtube] nie znaleziono kanalu")
        return {}

    stats   = _get_channel_stats(channel_id)
    uploads = stats.get("uploads_playlist", "")

    ostatnie = _get_last_videos(uploads, 15) if uploads else []
    top      = _get_top_videos(channel_id, 10)

    dane = {
        "ostatni_update": datetime.now(timezone.utc).isoformat(),
        "channel_id":     channel_id,
        "info_o_osobie":  BIRUTEQQ_INFO,
        "kanal":          stats,
        "ostatnie_filmy": ostatnie,
        "top_filmy":      top,
    }

    zapisz_yt(dane)
    print(f"[youtube] gotowe: {len(ostatnie)} ostatnich filmow, {len(top)} top filmow")
    return dane

def youtube_jako_tekst() -> str:
    dane = wczytaj_yt()
    if not dane:
        return "(brak danych youtube — jeszcze sie laduje)"

    czesci = []
    update = dane.get("ostatni_update", "?")[:16].replace("T", " ")
    czesci.append(f"INFO O BIRUTEQQ (update: {update} UTC):")
    czesci.append(dane.get("info_o_osobie", ""))

    kanal = dane.get("kanal", {})
    if kanal:
        czesci.append(f"\nKanal YouTube:")
        czesci.append(f"  Subskrypcje: {kanal.get('subskrypcje')}")
        czesci.append(f"  Liczba filmow: {kanal.get('filmy_total')}")
        czesci.append(f"  Wyswietlenia lacznie: {kanal.get('wyswietlen_lacznie')}")
        czesci.append(f"  Zalozony: {kanal.get('zalozony')}")
        if kanal.get("opis"):
            czesci.append(f"  Opis: {kanal['opis'][:300]}")

    ostatnie = dane.get("ostatnie_filmy", [])
    if ostatnie:
        czesci.append("\nOstatnie filmy:")
        for f in ostatnie:
            czesci.append(
                f"  [{f['data']}] {f['tytul']} | "
                f"{f.get('wyswietlen','?')} wysw | {f.get('lajki','?')} lajkow | "
                f"{f.get('komentarze','?')} koment | {f.get('dlugosc','?')}"
            )

    top = dane.get("top_filmy", [])
    if top:
        czesci.append("\nNajpopularniejsze filmy:")
        for f in top:
            czesci.append(
                f"  {f['tytul']} | {f.get('wyswietlen','?')} wysw | "
                f"{f.get('lajki','?')} lajkow | {f['data']}"
            )

    return "\n".join(czesci)

async def task_youtube():
    await asyncio.sleep(10)
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, odswiez_dane_youtube)
    except Exception as e:
        print(f"[task_youtube] start: {e}")
    while True:
        await asyncio.sleep(REFRESH_SECS)
        try:
            await loop.run_in_executor(None, odswiez_dane_youtube)
        except Exception as e:
            print(f"[task_youtube] refresh: {e}")