> **ℹ️ English version below 👇**

Dieses Repository stellt einen containerisierten FastAPI-basierten Proxy bereit, der **personenbezogene Daten (PII)** aus Benutzereingaben entfernt, bevor sie an die OpenAI Chat Completions API weitergeleitet werden. Es gewährleistet eine **DSGVO-konforme Nutzung von LLMs**, insbesondere in sensiblen Kontexten, in denen Namen, E-Mails, Telefonnummern oder Adressen gefiltert werden müssen.

---

## **Architekturübersicht**

```text
Benutzereingabe
   |
   v
[ FastAPI-Endpunkt ]
   |
   v
[ PII-Filter (Presidio + spaCy) ]
   |
   v
[ Bereinigte Anfrage ] ---> [ OpenAI API ]
                                   |
                                   v
                      [ KI-Antwort wird an den Benutzer zurückgegeben ]
```



Dieses Repository stellt einen containerisierten FastAPI-basierten Proxy bereit, der **personenbezogene Daten (PII)** aus Benutzereingaben entfernt, bevor sie an die OpenAI Chat Completions API weitergeleitet werden. Es gewährleistet eine **DSGVO-konforme Nutzung von LLMs**, insbesondere in sensiblen Kontexten, in denen Namen, E-Mails, Telefonnummern oder Adressen gefiltert werden müssen.

---

## **Architekturübersicht**

```text
Benutzereingabe
   |
   v
[ FastAPI-Endpunkt ]
   |
   v
[ PII-Filter (Presidio + spaCy) ]
   |
   v
[ Bereinigte Anfrage ] ---> [ OpenAI API ]
                                   |
                                   v
                      [ KI-Antwort wird an den Benutzer zurückgegeben ]
```

---

## **Verzeichnisstruktur**

```
gdpr_proxy_service/
├── app/
│   ├── __init__.py              # Macht den Ordner zu einem Python-Modul
│   ├── main.py                  # FastAPI-Server, definiert Endpunkte und Logik
│   ├── config.py                # Lädt OpenAI-Token aus der .env-Datei
│   ├── pii_filter.py            # PII-Erkennung & Redaktionslogik mit Presidio
│   ├── openai_proxy.py          # Sendet bereinigte Anfragen asynchron an OpenAI
├── Dockerfile                   # Docker-Bauanleitung
├── requirements.txt             # Python-Abhängigkeiten
├── .env                         # Umgebungsvariablen (OPENAI_API_KEY)
├── TestOpenAI.py                # Testet Chat-Endpunkt mit vollständigem Proxyfluss
├── TestScript.py                # Testet lediglich die Redaktionslogik
└── README.md                    # Dieses Dokument
```

---

## **Dateierklärungen**

| Datei | Zweck |
|-------|-------|
| `main.py` | FastAPI-Server, definiert `/analyze` und `/v1/chat/completions` |
| `pii_filter.py` | Lädt spaCy-Modelle, konfiguriert benutzerdefinierte Presidio-Erkenner |
| `openai_proxy.py` | Leitet bereinigte Anfragen an OpenAI weiter |
| `config.py` | Lädt `OPENAI_API_KEY` und `OPENAI_API_URL` aus der `.env`-Datei |
| `TestOpenAI.py` | Führt vollständigen Endpunkt-Test durch |
| `TestScript.py` | Testet nur die Text-Redaktion über `/analyze` |
| `.env` | Definiert OpenAI-Schlüssel: `OPENAI_API_KEY=sk-...` |
| `Dockerfile` | Erstellt ein Image, um die App im Container auszuführen |
| `requirements.txt` | Definiert alle benötigten Bibliotheken |

---

## **Installation und Verwendung**

### 1. Repository klonen und konfigurieren

```bash
git clone https://github.com/your-org/gdpr_proxy_service.git
cd gdpr_proxy_service
echo "OPENAI_API_KEY=sk-..." > .env
```

### 2. Docker-Image bauen

```bash
docker build -t gdpr_proxy .
```

### 3. Container ausführen

```bash
docker run -e OPENAI_API_KEY=sk-... -p 8000:8000 gdpr_proxy
```

Oder alternativ `.env` nutzen:

```bash
docker run --env-file .env -p 8000:8000 gdpr_proxy
```

### 4. Redaktions-API testen

```bash
curl -X POST http://localhost:8000/analyze      -H "Content-Type: application/json"      -d '{"text": "Mein Name ist John Doe und meine E-Mail ist john@example.com"}'
```

### 5. Chat-Komplettions-Endpunkt testen

```bash
python TestOpenAI.py
```

---

## **Redaktionsstrategie**

Es wird [Microsoft Presidio](https://github.com/microsoft/presidio) verwendet, mit benutzerdefinierten `PatternRecognizer` für **Deutsch und Englisch**. Es werden folgende Entitäten entfernt:

- Namen (`PERSON`)
- E-Mail-Adressen
- Telefonnummern (international)
- Kreditkarteninformationen
- Orte

Die Sprache wird automatisch mit spaCy erkannt und das entsprechende Modell geladen (`en_core_web_lg`, `de_core_news_lg`).

---

## **Ziele und Vorteile**

- **DSGVO-konform**: Keine PII wird an OpenAI weitergeleitet.
- **Sprachsensitiv**: Erkennt automatisch Deutsch oder Englisch.
- **Containerisiert**: Leicht in jeder Umgebung einsetzbar.
- **Erweiterbar**: Weitere Sprachen und Regeln einfach integrierbar.

---

## **Sicherheitshinweis**

Dieser Proxy ist für den **internen Gebrauch** vorgesehen. Bitte nicht ohne Authentifizierung und Rate-Limiting nach außen exponieren.

---

---



> **ℹ️ German version above 👆**

This repository provides a containerized FastAPI-based proxy that redacts **personally identifiable information (PII)** from user prompts before forwarding them to the OpenAI Chat Completions API. It ensures **GDPR-compliant usage of LLMs**, particularly in sensitive contexts where names, emails, phone numbers, or addresses must be filtered.

---

## **Architecture Overview**

```text
User Prompt
   |
   v
[ FastAPI Endpoint ]
   |
   v
[ PII Redactor (Presidio + spaCy) ]
   |
   v
[ Sanitized Request ] ---> [ OpenAI API ]
                                   |
                                   v
                          [ AI Response Returned to User ]
```



This repository provides a containerized FastAPI-based proxy that redacts **personally identifiable information (PII)** from user prompts before forwarding them to the OpenAI Chat Completions API. It ensures **GDPR-compliant usage of LLMs**, particularly in sensitive contexts where names, emails, phone numbers, or addresses must be filtered.

---

## **Architecture Overview**

```text
User Prompt
   |
   v
[ FastAPI Endpoint ]
   |
   v
[ PII Redactor (Presidio + spaCy) ]
   |
   v
[ Sanitized Request ] ---> [ OpenAI API ]
                                   |
                                   v
                          [ AI Response Returned to User ]
```

---

## **Directory Structure**

```
gdpr_proxy_service/
├── app/
│   ├── __init__.py              # Makes the app folder a Python module
│   ├── main.py                  # FastAPI server, routes and flow orchestration
│   ├── config.py                # Loads and stores OpenAI credentials from .env
│   ├── pii_filter.py            # AnalyzerEngine & PII redaction logic using Presidio
│   ├── openai_proxy.py          # Async OpenAI API forwarder via httpx
├── Dockerfile                   # Docker container build instructions
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (OPENAI_API_KEY)
├── TestOpenAI.py                # Host-side test script: sends chat prompt to /v1/chat/completions
├── TestScript.py                # Simpler test script for analyzing redaction only
└── README.md                    # You are here
```

---

## **What Each File Does**

| File | Purpose |
|------|---------|
| `main.py` | Main FastAPI server, defines `/analyze` and `/v1/chat/completions` routes |
| `pii_filter.py` | Loads multilingual spaCy models and builds PII recognizers using Presidio |
| `openai_proxy.py` | Sends HTTP request to OpenAI endpoint after redaction |
| `config.py` | Loads `.env` variables like `OPENAI_API_KEY` and API URL |
| `TestOpenAI.py` | Host-side script to test end-to-end chat completion logic |
| `TestScript.py` | Sends a text input to `/analyze` to verify redaction works |
| `.env` | Define your OpenAI key here: `OPENAI_API_KEY=sk-...` |
| `Dockerfile` | Build and run your app with `uvicorn` inside Docker |
| `requirements.txt` | All libraries needed for PII detection, FastAPI, and HTTP communication |

---

## **Setup & Usage**

### 1. Clone and Configure

```bash
git clone https://github.com/your-org/gdpr_proxy_service.git
cd gdpr_proxy_service
echo "OPENAI_API_KEY=sk-..." > .env
```

### 2. Build the Docker Image

```bash
docker build -t gdpr_proxy .
```

### 3. Run the Container

```bash
docker run -e OPENAI_API_KEY=sk-... -p 8000:8000 gdpr_proxy
```

Or, if using `.env` automatically:

```bash
docker run --env-file .env -p 8000:8000 gdpr_proxy
```

### 4. Test the Redaction API

```bash
curl -X POST http://localhost:8000/analyze      -H "Content-Type: application/json"      -d '{"text": "My name is John Doe and email is john@example.com"}'
```

### 5. Test End-to-End Chat Completion

Run from host:

```bash
python TestOpenAI.py
```

---

## **Redaction Strategy**

The service uses [Microsoft Presidio](https://github.com/microsoft/presidio) with custom `PatternRecognizer` rules for German and English. It removes:

- Names (`PERSON`)
- Email addresses
- Phone numbers (international format)
- Credit cards
- Locations

Language is auto-detected using spaCy and the correct model is applied (`en_core_web_lg`, `de_core_news_lg`).

---

## **Goals & Benefits**

- **GDPR-compliant**: Never sends PII to external OpenAI APIs.
- **Language-aware**: Handles both English and German inputs.
- **Containerized**: Easy to deploy in secure and scalable environments.
- **Extensible**: You can add recognizers for more languages or PII types.

---

## **Security Note**

This proxy is designed for **internal use** to protect user data. Do not expose it directly to untrusted external traffic without proper rate limiting and authentication.

---
---

## 🧠 Erweiterung: Prominente Personen (Deutsch)

Das System verwendet jetzt eine vorab gespeicherte JSON-Datei mit über **125.000 deutschen prominenten Personen** (aus Wikidata), um sicherzustellen, dass öffentlich bekannte Namen **nicht** fälschlicherweise geschwärzt werden.

- Quelle: [Wikidata SPARQL](https://query.wikidata.org/)
- Berufe: Politiker, Schauspieler, Musiker, Sportler, Autoren usw.
- Format: `data/public_figures_de.json`

Beispiel:
```json
[{"personLabel":"Angela Merkel"}, {"personLabel":"Friedrich Merz"}, {"personLabel":"Steffi Graf"}]
```

Diese Liste wird beim Start der Anwendung geladen und mit PII-Ergebnissen verglichen. Wenn ein erkannter Name in dieser Liste ist, wird er **nicht geschwärzt**.

---

## 📁 Zusätzliche Dateien

| Datei | Zweck |
|-------|-------|
| `data/public_figures_de.json` | Liste von öffentlichen Personen (Deutschland) zur Ausnahmelogik bei der Redaktion |
| `public_figures_loader.py` | Lädt JSON-Datei mit bekannten Namen und stellt sie dem Filter zur Verfügung |

---

## 🧠 Extension: Public Figures Dataset (English)

The system now uses a pre-loaded JSON dataset with over **125,000 German public figures** (from Wikidata) to ensure well-known names are **not mistakenly redacted**.

- Source: [Wikidata SPARQL](https://query.wikidata.org/)
- Occupations: Politicians, actors, musicians, authors, athletes, etc.
- Format: `data/public_figures_de.json`

Example:
```json
[{"personLabel":"Angela Merkel"}, {"personLabel":"Friedrich Merz"}, {"personLabel":"Steffi Graf"}]
```

This file is loaded during startup and compared against detected names. If a match is found, the name is **preserved** in the prompt sent to OpenAI.

---

## 📁 Additional Files

| File | Purpose |
|------|---------|
| `data/public_figures_de.json` | Stores list of public German figures to skip redaction |
| `public_figures_loader.py` | Loads and parses this list for redaction exemption |