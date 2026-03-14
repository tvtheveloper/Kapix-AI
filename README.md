# kapix — Discord Bot

Bot Discordowy pisany w Pythonie. Reaguje na wiadomości z użyciem AI, śledzi statystyki piłkarskie i kanał YouTube, obsługuje losowanie nagród za levele oraz system VoteMute.

## Funkcje

- **AI na czacie** — odpowiada gdy ktoś go pingnie lub napisze jego imię, bazując na historii serwera
- **Pamięć serwera** — zapamiętuje użytkowników i tematy rozmów (`mozg.json`)
- **Losowanie nagród** — automatycznie losuje nagrodę po awansie na level (w wątku pod wiadomością bota levelowego)
- **VoteMute** — społecznościowe wyciszanie użytkowników głosowaniem
- **Dane piłkarskie** — aktualne tabele, wyniki i statystyki PSG z 6 lig (co 12h)
- **YouTube** — śledzenie kanału Biruteqq (co 12h)

## Wymagania

- Python 3.10+
- Konto na [OpenRouter](https://openrouter.ai/) (klucz API do modelu LLM)
- Bot Discord z uprawnieniami: `Send Messages`, `Manage Threads`, `Moderate Members`, `Read Message History`

## Instalacja

```bash
git clone https://github.com/TWOJ_NICK/kapix.git
cd kapix
pip install -r requirements.txt
```

Stwórz plik `.env` w katalogu projektu:

```env
DISCORD_TOKEN=twoj_token_discord
```

Następnie w `main.py` uzupełnij swój klucz OpenRouter:

```python
OPENROUTER_KEY = "sk-or-..."
```

Oraz ID kanałów swojego serwera:

```python
KANAL_GLOWNY    = ...
KANAL_DODATKOWY = ...
KANAL_STARTIT   = ...   # kanal gdzie bot levelowy wysyla wiadomosci o awansie
```

## Uruchomienie

```bash
python app.py
```

## Komendy

| Komenda | Uprawnienia | Opis |
|---|---|---|
| `$w=<tekst>` | admin | Wyślij wiadomość jako bot (usuwa oryginalną) |
| `$mozg_flush` | admin | Ręcznie zapisz bufor do pamięci |
| `$votemute_toggle` | admin | Włącz/wyłącz VoteMute |
| `$losuj_<level>` | admin | Ręcznie przetestuj losowanie nagrody |
| `$votemute <@user>` | wszyscy | Rozpocznij głosowanie na muta |

## Struktura plików

```
kapix/
├── app.py            # launcher
├── main.py           # logika bota
├── pilka.py          # dane piłkarskie
├── youtube.py        # dane YouTube
├── requirements.txt
├── .env              # NIE commituj tego pliku
└── .gitignore
```

## Licencja

MIT — szczegóły w pliku [LICENSE](LICENSE).
