import requests
import json
import smtplib
from email.message import EmailMessage
import os

# URL da API e Token inspirável TESTE2
url = "#################"
headers = {"Authorization": "Bearer #################################"}

# Requisição
response = requests.get(url, headers=headers)

# Verificando se a requisição deu certo
if response.status_code == 200:
    data = response.json()
    
# Configurando o server de Email
SMTP_SERVER = "###############"
SMTP_PORT = 587
EMAIL_SENDER = "#################"
EMAIL_PASSWORD = "############"
EMAIL_RECIPIENT = "#################" 
EMAIL_SUBJECT = "Novos Leads Alvocom"

# IDs já processados
ID_FILE = "ids_processados.json"

# Função para carregar os IDs já processados
