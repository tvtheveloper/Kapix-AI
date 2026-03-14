# Kapix AI

![Kapix AI Banner](https://i.postimg.cc/nhP8jKDg/KAPIX-AI.png)

Polski bot Discord oparty na modelu językowym. Uczestniczy w rozmowach, śledzi aktualne wyniki piłkarskie, obsługuje losowanie nagród za levele oraz system demokratycznego wyciszania użytkowników.

---

## ✨ Funkcje

**🤖 Rozmowy oparte na AI**
Kapix odpowiada gdy zostanie spingowany lub ktoś napisze jego imię. Korzysta z modelu LLaMA 3.3 70B przez OpenRouter. Buduje pamięć serwera — zapamiętuje użytkowników, tematy i kontekst rozmów.

**⚽ Dane piłkarskie**
Co 12 godzin pobiera aktualne tabele, wyniki i statystyki strzelców z Champions League, Ligue 1, Premier League, Bundesligi, Serie A oraz La Liga. Śledzi również pełny terminarz i skład PSG.

**🎰 Losowanie nagród za levele**
Po awansie na level bot automatycznie tworzy wątek pod wiadomością i przeprowadza animowane losowanie nagrody. Szanse rosną wraz z poziomem.

**📺 Monitoring YouTube**
Śledzi kanał Biruteqq — statystyki, ostatnie filmy, najpopularniejsze materiały.

---

## 🚀 Instalacja

```bash
git clone https://github.com/TWOJ_NICK/kapix.git
cd kapix
pip install -r requirements.txt
```

Stwórz plik `.env` w katalogu projektu i uzupełnij wszystkie wartości:

```env
DISCORD_TOKEN=twoj_token_discord

OPENROUTER_KEY=sk-or-...
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct

KANAL_GLOWNY=id_kanalu        # główny kanał — bot odpowiada na każdą wiadomość z jego imieniem
KANAL_DODATKOWY=id_kanalu     # drugi kanał — mniejsza szansa odpowiedzi (15%)
KANAL_STARTIT=id_kanalu       # kanał bota levelowego — tu wykrywa awanse

DOZWOLENI=id1,id2,id3         # ID użytkowników z uprawnieniami admina (oddzielone przecinkami)
```

Uruchomienie:

```bash
python app.py
```

---

## 🛠️ Komendy

```
$w=tekst              — wyślij wiadomość jako bot          [admin]
$losuj_<level>        — testuj losowanie nagrody           [admin]
```

---

## 📋 Wymagania

- Python 3.10+
- Uprawnienia bota: `Send Messages`, `Create Public Threads`, `Moderate Members`
- Klucz API [OpenRouter](https://openrouter.ai/)

---

## 📄 Licencja

MIT — szczegóły w pliku [LICENSE](LICENSE).
