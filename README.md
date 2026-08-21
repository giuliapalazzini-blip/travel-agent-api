# Travel Agent API

- Python 3.12
- Poetry
- FastAPI
- LangChain
- LangGraph
- OpenAI
- SerpApi
- Pydantic

Le chiavi API vengono salvate nel file `.env`:

OPENAI_API_KEY=
SERPAPI_API_KEY=

Il file `.env` è inserito nel `.gitignore`.

Per installare le dipendenze:

```bash
poetry install
```

Per avviare il progetto:

```bash
poetry run uvicorn travel_agent_api.main:app --reload --app-dir src --port 8080
```

La documentazione Swagger è disponibile su:

```text
http://127.0.0.1:8080/docs
```

## Tools

Nel progetto sono presenti quattro tools:

- `flights_finder`: ricerca dei voli tramite SerpApi
- `hotels_finder`: ricerca degli hotel tramite SerpApi
- `chain_travel_plan`: creazione di un piano di viaggio
- `chain_historical_expert`: informazioni storiche e culturali su una località

Gli input dei tools vengono gestiti e validati tramite Pydantic.

## Agent

L'endpoint principale è:

```text
POST /chat/travel-agent
```
Durante lo sviluppo ho aggiunto alcune `print()` per controllare nel terminale il funzionamento dell'Agent e dei diversi tools.

## Test

Ho testato l'API tramite Swagger verificando separatamente:

- ricerca voli
- ricerca hotel
- generazione di un piano di viaggio
- informazioni storiche e culturali

I test dell'endpoint `POST /chat/travel-agent` hanno restituito stato `200 OK`.

## Client Laravel

FastAPI viene eseguito sulla porta `8080`, mentre Laravel sulla porta `8001`.

```bash
php artisan serve --host=127.0.0.1 --port=8001
```

Il client Laravel invia i messaggi all'endpoint FastAPI `POST /chat/travel-agent` e visualizza la risposta nell'interfaccia della chat.