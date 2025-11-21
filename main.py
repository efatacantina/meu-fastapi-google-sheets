from fastapi import FastAPI
from pydantic import BaseModel
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# ----- Google Sheets Setup -----
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1EzQ91B6cusEoDGc3onAIfwDdepvo38xld0agiHBwUyM"
RANGE = "Página1!A:C"

CREDENTIALS_PATH = "/etc/secrets/credentials.json"

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_PATH, scopes=SCOPES
)

service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()

class Pedido(BaseModel):
    produto: str
    quantidade: int
    preco: float

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.post("/registrar")
def registrar_pedido(pedido: Pedido):
    valores = [[pedido.produto, pedido.quantidade, pedido.preco]]
    req = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE,
        valueInputOption="USER_ENTERED",
        body={"values": valores},
    )
    req.execute()

    return {"status": "ok", "salvo": valores}

