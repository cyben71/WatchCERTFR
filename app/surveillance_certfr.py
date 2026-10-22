#!/usr/bin/env python
# coding: utf-8

# In[1]:


APPLICATION_NAME = "surveillance_certfr"


# In[ ]:


import sys
from pathlib import Path

# Remonter les dossiers jusqu'à trouver lib/init/init_code.py
def find_app_home(sentinel: str ="lib/bootstrap/bootstrap.py"):
    current = Path.cwd().resolve()
    root = current.root
    while current != root:
        if (current / sentinel).is_file():
            return current
        current = current.parent
    raise FileNotFoundError(f"Impossible de trouver le fichier sentinelle : {sentinel}")

# Trouver et ajouter APPLICATION_HOME au sys.path
APPLICATION_HOME = find_app_home()
sys.path.insert(0, str(APPLICATION_HOME))
#print(f"APPLICATION_HOME set to: {APPLICATION_HOME}")

from lib.bootstrap.bootstrap import init_env
epy = init_env()


# In[3]:


# import
import feedparser
import os
import certifi


# In[4]:


# variables
log = epy.log
yml = epy.cfgyaml

watch = yml.get("watch_list")
# print(watch)
excluding = yml.get("exclude")
# print(excluding)

email_on: bool = yml.get("email.enable")
# print(email_on)


# In[5]:


if email_on: 
    import smtplib
    from email.mime.multipart import MIMEMultipart      # MIMEMultipart send emails with both text content and attachments.
    from email.mime.text import MIMEText                # MIMEText for creating body of the email message.
    from email.mime.application import MIMEApplication  # MIMEApplication attaching application-specific data (like CSV files) to email messages.
    from email.utils import COMMASPACE
    from email.utils import formatdate
else:
    log.warning("Sending email alert is OFF")
    log.log("")


# ## Traitement

# In[6]:


log.log("==========================================")
log.log("=== Scan des avis & alertes du CERT-FR ===")
log.log("==========================================")
log.info(f"Liste des programmes surveillés : {watch}")
log.log("")


# ### Recherche des alertes et avis CERTFR

# In[7]:


# Force Python à utiliser le fichier de certificats de certifi pour éviter une erreur de type
# SSLCertVerificationError: certificate verify failed: unable to get local issuer certificate
os.environ['SSL_CERT_FILE'] = certifi.where()


# In[8]:


flag_email: bool = False

for feed in yml.get("feed"):

    log.info(f"{feed['name'].capitalize()} de sécurité: {feed['url']} ")
    try:
        parse = feedparser.parse(f"{feed['url']}/feed/")
    except Exception as err:
        log.error(f"Erreur de récupération du feed {feed['url']} - {err}")
        raise ValueError
    # print(parse)

    if len(parse)>0:
        for p in parse.entries:
            # print(f"{p['title']} - {p['link']}")
            id: str = p['link'].strip(feed["url"])
            title_lowercase: str = p['title'].lower()
            # print(title_lowercase)
            if any(terme in title_lowercase for terme in watch):
                log.log(f"{p['title']} - {id} -  {p['link']}")
                flag_email = True
        log.log("")
    else:
        log.warning(f"Aucune information remontées - {parse}")



# In[9]:


log.log("=== Fin du traitement ===")
log.log("")


# ### Alerting par email

# In[ ]:


if flag_email and email_on:
    smtp_server: str = yml.get('smtp.host')
    smtp_port: int = yml.get('smtp.port')
    sender_email: str = yml.get('smtp.user')
    sender_password: str = yml.get('smtp.password')
    recipient_email = yml.get('email.to')


    log_file: str = log.log_file
    log_filename: str = os.path.basename(epy.log.log_file)

    # MIMEMultipart() creates a container for an email message that can hold
    # different parts, like text and attachments and in next line we are
    # attaching different parts to email container like subject and others.
    message = MIMEMultipart()
    message['Subject'] = yml.get('email.subject')
    message['From'] = yml.get('email.from')
    message['To'] = COMMASPACE.join(recipient_email)
    message["Date"] = formatdate(localtime=True)
    body_part = MIMEText(yml.get('email.body'))
    message.attach(body_part)

    # #print(message)
    try:
        # section 1 to attach file
        # Attach the file with filename to the email
        with open(log_file,'rb') as file:
            message.attach(MIMEApplication(file.read(), Name=log_filename))

        # section 2 for sending email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            if yml.get('smtp.isTls'):
                server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
    except Exception as err:
        log.error(f"Echec d'envoi d'email")
        # DEBUG
        # print(message)

