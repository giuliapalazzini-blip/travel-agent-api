# Travel Agent API

Progetto finale della Specializzazione Coding AI.

Il progetto consiste nella realizzazione di un Travel Agent sviluppato in Python utilizzando FastAPI, LangChain e LangGraph.

L'applicazione espone delle API che permettono di interagire con un agente AI in grado di utilizzare diversi strumenti per fornire informazioni utili alla pianificazione di un viaggio.

## Tecnologie utilizzate

- Python 3.12
- Poetry
- FastAPI
- Uvicorn
- LangChain
- LangGraph
- OpenAI
- SerpApi
- python-dotenv

## Configurazione del progetto

Il progetto è stato creato e gestito tramite Poetry.

Sono state installate le dipendenze necessarie per FastAPI, LangChain, LangGraph, OpenAI e SerpApi.

Le chiavi API vengono gestite tramite un file `.env`:

- `OPENAI_API_KEY`
- `SERPAPI_API_KEY`

Il file `.env` è escluso dalla repository tramite `.gitignore` per evitare di pubblicare le chiavi API.

È presente anche un file `.env.example` che mostra le variabili necessarie senza contenere le chiavi reali.

## API FastAPI

È stata configurata un'applicazione FastAPI con middleware CORS.

È stata inoltre creata la cartella `routes` per la gestione degli endpoint dell'applicazione.

Prima di implementare l'agente completo è stata creata una route di prova per verificare il corretto funzionamento dell'API e della documentazione Swagger.

L'API è stata testata tramite:

`http://127.0.0.1:8000/docs`

## Tools

### Flights Finder

È stato creato il tool `flights_finder` per effettuare ricerche di voli tramite Google Flights utilizzando SerpApi.

Il tool riceve informazioni come aeroporto di partenza, aeroporto di arrivo e date del viaggio.

Gli input del tool vengono validati tramite modelli Pydantic, includendo aeroporto di partenza e arrivo, date, numero di adulti e bambini.

Come piccola attività di refactoring, il dizionario utilizzato per costruire la richiesta SerpApi è stato rinominato `search_params`, per distinguerlo più chiaramente dall'oggetto `params` ricevuto dalla funzione.

### Hotels Finder

È stato creato il tool `hotels_finder` per effettuare ricerche di hotel tramite Google Hotels utilizzando SerpApi.

Il tool utilizza destinazione, date di check-in e check-out e numero di adulti.

Gli input vengono validati tramite Pydantic e comprendono località, date di check-in e check-out, numero di adulti e bambini e classe dell'hotel.

È stata inoltre corretta la denominazione dello schema di input in `HotelsInputSchema` per rendere il codice più leggibile e coerente.

Sono state aggiunte ulteriori istruzioni `print()` per tracciare i parametri principali utilizzati durante le ricerche.

## Tracing

Per comprendere meglio il flusso di esecuzione dell'applicazione sono state aggiunte delle istruzioni `print()` all'interno dei tool.

Le stampe permettono di visualizzare nel terminale i principali parametri ricevuti e verificare quando viene completata una ricerca.

### Historical Expert

È stato creato il tool `chain_historical_expert`, che utilizza LangChain e OpenAI per fornire informazioni storiche e culturali su una destinazione.

Il tool riceve una località e genera una risposta con informazioni su monumenti, eventi storici, cultura e curiosità utili per il viaggiatore.

Anche in questo tool sono state aggiunte istruzioni `print()` per tracciare l'esecuzione e verificare quale località viene elaborata.

## Agent Service

È stato creato il servizio `Agent`, che rappresenta il componente centrale dell'applicazione.

L'Agent utilizza un modello OpenAI e LangGraph per scegliere dinamicamente quale strumento utilizzare in base alla richiesta dell'utente.

I tool disponibili sono:

- `flights_finder`
- `hotels_finder`
- `chain_travel_plan`
- `chain_historical_expert`

L'Agent è stato implementato utilizzando un ReAct Agent, in grado di ragionare sulla richiesta ricevuta e richiamare automaticamente gli strumenti necessari.

Sono state aggiunte istruzioni `print()` sia durante l'inizializzazione dell'Agent sia durante l'elaborazione dei messaggi, in modo da effettuare il tracing dell'esecuzione.

## Chat API

È stata implementata la route `POST /chat/travel-agent`.

La route riceve una lista di messaggi, li inoltra al servizio `Agent` e restituisce i messaggi generati durante l'esecuzione.

Sono state aggiunte istruzioni `print()` anche nella route per tracciare il numero di messaggi ricevuti e verificare il completamento della richiesta.

L'endpoint può essere testato tramite la documentazione Swagger disponibile all'indirizzo:

`http://127.0.0.1:8000/docs`

## Test dell'API

L'API è stata testata tramite la documentazione interattiva Swagger di FastAPI disponibile all'indirizzo:

`http://127.0.0.1:8000/docs`

È stato testato l'endpoint:

`POST /chat/travel-agent`

utilizzando una richiesta relativa alle principali attrazioni storiche di Roma.

Il Travel Agent ha elaborato correttamente la richiesta e l'API ha restituito una risposta con stato HTTP `200 OK`.

Durante il test è stato utilizzato il tracing tramite `print()` per verificare nel terminale l'inizializzazione dell'Agent, la ricezione del messaggio e l'esecuzione della richiesta.

Durante lo sviluppo è stata inoltre corretta la comunicazione tra la route FastAPI e il servizio Agent, utilizzando il metodo `invoke()` previsto dall'implementazione dell'Agent.

### Test ricerca voli

È stato testato il tool `flights_finder` tramite l'endpoint `POST /chat/travel-agent`.

La richiesta di prova prevedeva una ricerca di volo andata e ritorno da Roma Fiumicino (FCO) a Barcellona (BCN), dal 10 settembre 2026 al 14 settembre 2026, per 1 adulto.

L'Agent ha selezionato correttamente il tool `flights_finder` e ha utilizzato SerpApi per recuperare risultati reali da Google Flights.

Il test ha restituito stato HTTP `200 OK`.

La risposta finale ha mostrato diverse opzioni di volo con compagnia aerea, orari, durata, prezzo e link a Google Flights.

### Test ricerca hotel

È stato testato il tool `hotels_finder` tramite l'endpoint `POST /chat/travel-agent`.

La richiesta di prova prevedeva la ricerca di un hotel a Barcellona dal 10 settembre 2026 al 14 settembre 2026, per 1 adulto, con categoria di almeno 3 stelle.

L'Agent ha selezionato correttamente il tool `hotels_finder` e ha utilizzato SerpApi per recuperare risultati reali da Google Hotels.

Il test ha restituito stato HTTP `200 OK`.

La risposta ha incluso informazioni relative a strutture disponibili, prezzi, orari di check-in e check-out, valutazioni, servizi e posizione.

### Test generazione piano di viaggio

È stato testato il tool `chain_travel_plan` tramite l'endpoint `POST /chat/travel-agent`.

La richiesta di prova prevedeva l'organizzazione di un viaggio a Barcellona dal 10 settembre 2026 al 14 settembre 2026, per 2 adulti, con stile culturale e rilassante, budget di 1200 euro, attività legate a cultura, cibo e passeggiate e alimentazione senza glutine.

L'Agent ha selezionato correttamente il tool `chain_travel_plan`.

Il tool ha generato con successo un itinerario strutturato per 5 giorni, organizzato in attività per mattina, pomeriggio e sera.

L'output strutturato è stato validato tramite Pydantic e successivamente trasformato dall'Agent in una risposta leggibile in linguaggio naturale.

Il test ha restituito stato HTTP `200 OK`.

### Test esperto storico

È stato testato il tool `chain_historical_expert` tramite l'endpoint `POST /chat/travel-agent`.

La richiesta di prova riguardava la storia e le principali curiosità culturali del Colosseo di Roma.

L'Agent ha selezionato correttamente il tool `chain_historical_expert` e ha utilizzato la località `Colosseo, Roma` come parametro di input.

Il tool ha generato con successo informazioni storiche, architettoniche e culturali relative al Colosseo.

Il test ha restituito stato HTTP `200 OK`.

## Integrazione con il client Laravel

Per verificare il funzionamento completo dell'applicazione è stato utilizzato il client web Laravel fornito con il progetto.

L'API Python viene avviata tramite FastAPI sulla porta 8080:

```bash
poetry run uvicorn travel_agent_api.main:app --reload --app-dir src --port 8080