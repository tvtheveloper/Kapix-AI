# Kapix AI

![Kapix AI Banner]([https://url-do-twojego-obrazu.png](https://i.postimg.cc/nhP8jKDg/KAPIX-AI.png))

Polski bot Discord oparty na modelu językowym. Uczestniczy w rozmowach, śledzi aktualne wyniki piłkarskie, obsługuje losowanie nagród za levele oraz system demokratycznego wyciszania użytkowników.

---

## ✨ Funkcje

**🤖 Rozmowy oparte na AI**
Kapix odpowiada gdy zostanie spingowany lub ktoś napisze jego imię. Korzysta z modelu LLaMA 3.3 70B przez OpenRouter. Buduje pamięć serwera — zapamiętuje użytkowników, tematy i kontekst rozmów.

**⚽ Dane piłkarskie**
Co 12 godzin pobiera aktualne tabele, wyniki i statystyki strzelców z Champions League, Ligue 1, Premier League, Bundesligi, Serie A oraz La Liga. Śledzi również pełny terminarz i skład PSG.

**🎰 Losowanie nagród za levele**
Po awansie na level bot automatycznie tworzy wątek pod wiadomością i przeprowadza animowane losowanie nagrody. Szanse rosną wraz z poziomem.

**🗳️ VoteMute**
Użytkownicy mogą głosować za wyciszeniem kogoś. Czas muta i wymagana liczba głosów są losowe — od 1 minuty do tygodnia.

**📺 Monitoring YouTube**
Śledzi kanał Biruteqq — statystyki, ostatnie filmy, najpopularniejsze materiały.

---

## 🚀 Instalacja

```bash
git clone https://github.com/TWOJ_NICK/kapix.git
cd kapix
pip install -r requirements.txt
```

Stwórz plik `.env` w katalogu projektu:

```
DISCORD_TOKEN=wklej_token_tutaj
```

W `main.py` uzupełnij klucz [OpenRouter](https://openrouter.ai/) oraz ID kanałów:

```python
OPENROUTER_KEY  = "sk-or-..."

KANAL_GLOWNY    = ...   # główny kanał — bot odpowiada na każdą wiadomość z jego imieniem
KANAL_DODATKOWY = ...   # drugi kanał — mniejsza szansa odpowiedzi (15%)
KANAL_STARTIT   = ...   # kanał bota levelowego — tu wykrywa awanse
```

Uruchomienie:

```bash
python app.py
```

---

## 🛠️ Komendy

```
$votemute @user       — rozpocznij głosowanie na muta
$w=tekst              — wyślij wiadomość jako bot          [admin]
$votemute_toggle      — włącz / wyłącz system votemute    [admin]
$mozg_flush           — ręcznie zapisz pamięć serwera     [admin]
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
