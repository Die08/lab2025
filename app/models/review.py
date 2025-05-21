'''Il file review.py serve a definire uno schema di validazione (un modello Pydantic) per il
 campo “review” utilizzato nelle API di gestione dei libr'''
from pydantic import BaseModel, Field
#BaseModel: classe base di Pydantic per creare modelli che validano e serializzano i dati.
#Field: permette di aggiungere vincoli (metadati) sui campi.
from typing import Annotated
#Annotated: combina il tipo Python (int) con i metadati di validazione review

class Review(BaseModel):
    review: Annotated[int, Field(ge=1, le=5)]

#Si crea un modello Pydantic chiamato Review con un solo attributo:
#review: un intero che deve essere compreso tra 1 e 5 (ge=1, le=5).
#Quando FastAPI riceve una richiesta che utilizza questo schema (ad es. nell’endpoint POST /books/{id}/review), Pydantic si occupa di:
#Verificare che il campo review sia presente.
#Controllare che sia un numero intero.
#Assicurarsi che rientri nel range 1–5; altrimenti restituisce automaticamente
# un errore 422 Unprocessable Entity con dettagli sul vincolo violato