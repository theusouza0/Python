import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time

# Configuração da API
url = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
headers = {
    "Authorization": "Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}

# Configuração do servidor de e-mail
SMTP_SERVER = "xxxxxxxxxxxxxxxx"
SMTP_PORT = 587
EMAIL_SENDER = "xxxxxxxxxxxxxxxxxxxx"
EMAIL_PASSWORD = "xxxxxxxxxxxxxxx"
EMAIL_RECIPIENTS = ["xxxxxxxxxxxxxxxxxxxxxxx"]
EMAIL_SUBJECT = "Novos Leads Alvocom"

# Arquivo onde os leads já enviados serão armazenados
ID_STORAGE_FILE = "enviados.json"

# Tratamento do horário
horario_local = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# Carrega os leads que já foram enviados (ID, Nome e E-mail).
def carregar_leads_enviados():
    if os.path.exists(ID_STORAGE_FILE):
        with open(ID_STORAGE_FILE, "r") as f:
            try:
                return json.load(f)  # Retorna a lista
            except json.JSONDecodeError:
                return []
    return []

# Salva os leads que já foram enviados
def salvar_leads_enviados(leads):
    with open(ID_STORAGE_FILE, "w") as f:
        json.dump(leads, f, indent=4)

# Consulta a API, salva novos leads e envia e-mails sem repetir emails já enviados.
def noRepeatEmail():
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extrai os leads da resposta
        leads = data.get("data", [])

        if not leads:
            print("Nenhum lead encontrado na API.")
            time.sleep(5)
            return

        # Carrega os leads já enviados
        leads_enviados = carregar_leads_enviados()
        emails_enviados = {lead["email"] for lead in leads_enviados}  # Conjunto de emails já enviados

        # Lista para armazenar novos leads a serem enviados
        novos_leads = []
        novos_leads_enviados = leads_enviados.copy()  # Copia os leads já enviados
        emails_processados = set()  # Conjunto para evitar duplicatas na mesma execução

        for lead in leads:
            lead_id = lead["id"]
            nome = lead["attributes"].get("nome", "N/A")
            email = lead["attributes"].get("email", "N/A")

            # Se o email já foi enviado ou já está na lista da execução atual, ignora
            if email in emails_enviados or email in emails_processados:
                continue

            # Adiciona à lista de novos leads
            novo_lead = {"id": lead_id, "nome": nome, "email": email}
            novos_leads.append(novo_lead)
            novos_leads_enviados.append(novo_lead)  # Atualiza lista de leads enviados
            emails_processados.add(email)  # Marca o email como processado

        # Atualiza o arquivo com os novos leads enviados
        salvar_leads_enviados(novos_leads_enviados)

        # Se não houver novos leads, não envia e-mail
        if not novos_leads:
            print(f"({horario_local}) Nenhum novo lead encontrado. Nenhum e-mail será enviado.")
            time.sleep(5)
            return

        # Monta o corpo do e-mail
        email_body = "Novos Leads:\n\n"
        for lead in novos_leads:
            email_body += f"ID: {lead['id']}\n"
            email_body += f"Nome: {lead['nome']}\n"
            email_body += f"E-mail: {lead['email']}\n"
            email_body += "-" * 30 + "\n"

        # Criando a mensagem de e-mail
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(EMAIL_RECIPIENTS)
        msg["Subject"] = EMAIL_SUBJECT
        msg.attach(MIMEText(email_body, "plain"))

        # Enviando o e-mail
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENTS, msg.as_string())
            print(f"({horario_local}) E-mail enviado com sucesso! ")
            time.sleep(5)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar API: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Executar a função
noRepeatEmail()
