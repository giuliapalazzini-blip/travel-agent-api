from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from travel_agent_api.routes import chat_router

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Gestore eccezioni per intercettare body vuoti o malformati prima che causino un crash 500
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
  return JSONResponse(
      status_code=status.HTTP_400_BAD_REQUEST,
      content={
          "message": (
              "Payload non valido o body vuoto. Fornire una lista di messaggi"
              " corretta."
          ),
          "errors": exc.errors(),
      },
  )


app.include_router(chat_router.router, tags=["Chat"], prefix="/chat")