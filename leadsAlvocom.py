# Lista de bibliotecas
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Configuração da API
BASE_URL = "xxxxxxxxxxxxxxxx"
HEADERS = {
    "Authorization": "Bearer xxxxxxxxxxxxxxxxxxxxxx"
}

# Configuração do e-mail
SMTP_SERVER = "xxxxxxxxxxxxxxxxxxxxxxx"
SMTP_PORT = 587
EMAIL_SENDER = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
EMAIL_PASSWORD = "xxxxxxxxxxxxxxxxxxxxxxxx"
EMAIL_RECIPIENTS = ["xxxxxxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxxxxxx"]
EMAIL_SUBJECT = "Novos Leads"

# Arquivo onde os IDs já enviados serão armazenados
ID_STORAGE_FILE = "enviados.json"

# Função para carregar IDs já enviados
def carregar_ids_enviados():
    if os.path.exists(ID_STORAGE_FILE):
        with open(ID_STORAGE_FILE, "r") as f:
            return set(json.load(f))
    return set()

# Função para salvar os IDs já enviados
def salvar_ids_enviados(ids):
    with open(ID_STORAGE_FILE, "w") as f:
        json.dump(list(ids), f)

# Função para buscar leads em todas as páginas
def buscar_todos_leads():
    page = 1
    page_size = 100
    leads = []

    while True:
        url = f"{BASE_URL}?pagination[page]={page}&pagination[pageSize]={page_size}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        data = response.json()
        pagina_leads = data.get("data", [])

        if not pagina_leads:
            break  # Sai do loop se não houver mais leads

        leads.extend(pagina_leads)
        page += 1

    return leads

# Função principal
def processar_leads():
    try:
        # Buscar todos os leads paginados
        leads = buscar_todos_leads()

        # Carregar IDs já enviados
        ids_enviados = carregar_ids_enviados()

        # Filtrar apenas os novos leads
        novos_leads = [
            {
                "id": lead["id"],
                "nome": lead["attributes"].get("nome", "N/A"),
                "email": lead["attributes"].get("email", "N/A"),
            }
            for lead in leads if lead["id"] not in ids_enviados
        ]

        if not novos_leads:
            print("Nenhum novo lead encontrado. Nenhum e-mail será enviado.")
            return

        # Montar o corpo do e-mail
        email_body = "Novos Leads:\n\n"
        for lead in novos_leads:
            email_body += f"ID: {lead['id']}\n"
            email_body += f"Nome: {lead['nome']}\n"
            email_body += f"E-mail: {lead['email']}\n"
            email_body += "-" * 30 + "\n"

        # Criar a mensagem de e-mail
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(EMAIL_RECIPIENTS)
        msg["Subject"] = EMAIL_SUBJECT
        msg.attach(MIMEText(email_body, "plain"))

        # Enviar o e-mail
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENTS, msg.as_string())

        print("E-mail enviado com sucesso!")

        # Atualizar os IDs enviados
        ids_enviados.update(lead["id"] for lead in novos_leads)
        salvar_ids_enviados(ids_enviados)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar API: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Executar a função
if __name__ == "__main__":
    processar_leads()
