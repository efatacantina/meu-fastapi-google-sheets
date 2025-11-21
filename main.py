from fastapi import FastAPI
from pydantic import BaseModel
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ----- CORS -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Google Sheets Setup -----
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1EzQ91B6cusEoDGc3onAIfwDdepvo38xld0agiHBwUyM"
RANGE = "Página1!A:C"

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scopes=SCOPES
)

service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()

class Pedido(BaseModel):
    produto: str
    quantidade: int
    preco: float

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

