# 🤖 Discord AI Bot

Nowoczesny bot Discord napisany w Pythonie, który łączy **AI chat, dane piłkarskie oraz integrację z YouTube** w jednym projekcie.

Bot został zaprojektowany tak, aby był **lekki, szybki i łatwy do rozbudowy**.

---

# ✨ Funkcje

### 💬 AI Chat

Bot potrafi odpowiadać na wiadomości użytkowników przy użyciu modelu AI.

Możliwe zastosowania:

* rozmowy z botem
* pomoc w serwerze
* generowanie tekstu

---

### ⚽ Dane piłkarskie

Bot może pobierać dane o piłce nożnej z API:

* tabele lig
* informacje o drużynach
* zapisywanie danych do pliku

---

### 📺 YouTube

Bot potrafi pobierać dane o kanałach YouTube:

* statystyki kanału
* podstawowe informacje
* zapis danych

---

### 💾 System zapisu danych

Bot przechowuje dane w plikach JSON:

| Plik           | Opis            |
| -------------- | --------------- |
| `mozg.json`    | dane systemu AI |
| `pilka.json`   | dane piłkarskie |
| `youtube.json` | dane YouTube    |

---

# 🧱 Struktura projektu

```
project/
│
├── main.py
├── app.py
├── pilka.py
├── youtube.py
│
├── mozg.json
├── pilka.json
├── youtube.json
│
└── requirements.txt
```

---

# 🚀 Instalacja

### 1️⃣ Pobierz repozytorium

```
git clone https://github.com/TWOJE_REPO
cd TWOJE_REPO
```

### 2️⃣ Zainstaluj biblioteki

```
pip install -r requirements.txt
```

### 3️⃣ Dodaj token bota

Ustaw zmienną środowiskową:

```
DISCORD_TOKEN=twoj_token
```

---

# ▶️ Uruchomienie

```
python main.py
```

Bot uruchomi się i po chwili będzie online na Twoim serwerze Discord.

---

# ⚙️ Wymagania

* Python **3.10 lub nowszy**
* biblioteki z `requirements.txt`

---

# 🔒 Bezpieczeństwo

Nigdy nie publikuj w repozytorium:

* tokena Discord
* kluczy API
* danych prywatnych

---

# 🛠 Rozwój projektu

Projekt jest modularny, więc możesz łatwo dodawać nowe funkcje:

* nowe komendy
* nowe API
* system ekonomii
* mini gry

---

# 📜 Licencja

Projekt open-source – możesz go dowolnie modyfikować i rozwijać.
