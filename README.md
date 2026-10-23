# WatchCERTFR

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](#-prérequis)

**WatchCERTFR** est un outil de veille qui surveille les publications du [CERT-FR](https://www.cert.ssi.gouv.fr/) (avis, alertes et menaces/incidents) et repère celles qui concernent **les produits que vous utilisez**.

Il lit les flux RSS du CERT-FR, filtre les publications dont le titre mentionne un des mots-clés de votre liste de surveillance, écrit le résultat dans un fichier de log et, si vous l'activez, **vous l'envoie par e-mail** (log en pièce jointe).

> Le projet repose sur le socle [EssencePy](https://github.com/cyben71/EssencePy) : chargement de la configuration, gestion de l'environnement, logs et exécution multiplateforme.

---

## 🚀 Fonctionnalités

- 📡 **Lecture de plusieurs flux CERT-FR** : avis, alertes, menaces et incidents (configurables).
- 🎯 **Filtrage par liste de surveillance** (`watch_list`) sur le titre des publications.
- 📧 **Alerte e-mail optionnelle** via SMTP (STARTTLS), avec le log joint au message.
- 📝 **Logs fichier + console** : un fichier par jour, rotation automatique.
- 🔐 **Secrets hors du code** : identifiants SMTP dans un fichier `.env`.
- 🖥️ **Multiplateforme** : Windows, Linux et macOS.
- 📓 **Notebook ou script** : le même code s'exécute dans Jupyter ou en programme Python autonome.

---

## 📁 Structure du projet

```
WatchCERTFR/
├── app/                      # Programme exécutable (surveillance_certfr.py)
├── conf/
│   ├── application.yaml      # Configuration de l'application (flux, mots-clés, SMTP, e-mail)
│   ├── application.properties# Propriétés lues par ConfigProperties (voir note ci-dessous)
│   ├── env.conf              # Environnement Python (chemins des binaires, CA_BUNDLE)
│   └── requirements.txt      # Dépendances Python
├── lib/
│   └── bootstrap/            # Socle EssencePy (config, env, logs, calendrier, doc...)
├── log/                      # Logs (créé automatiquement)
├── notebooks/                # Notebook source (surveillance_certfr.ipynb)
├── scripts/
│   ├── shell/                # Scripts Linux / macOS
│   └── powershell/           # Scripts Windows
├── .env                      # Identifiants SMTP (ne pas versionner avec de vraies valeurs)
└── README.md
```

---

## ✅ Prérequis

- **Python 3.12 ou supérieur** (testé avec 3.12.8 sous Windows).
- Accès Internet vers `www.cert.ssi.gouv.fr`.
- Pour les alertes e-mail : un serveur SMTP et un compte d'envoi.

Dépendances (`conf/requirements.txt`) :

| Paquet | Rôle |
|--------|------|
| `pyyaml` | Lecture de `application.yaml` |
| `python-dotenv` | Chargement du fichier `.env` |
| `feedparser` | Lecture des flux RSS du CERT-FR |
| `certifi` | Certificats TLS (évite les erreurs `SSLCertVerificationError`) |
| `jupyter` | *(optionnel, commenté par défaut)* exécution et conversion des notebooks |

---

## 🛠️ Installation

1. **Cloner** le dépôt :
   ```bash
   git clone https://github.com/cyben71/WatchCERTFR.git
   cd WatchCERTFR
   ```

2. **Renseigner l'interpréteur Python** dans `conf/env.conf` :

   | Variable | Système | Exemple |
   |----------|---------|---------|
   | `PARENT_PYTHON_HOME` | Linux / macOS | `/opt/python/3.12.8` |
   | `PARENT_PYTHON_EXE` | Linux / macOS | `python3` |
   | `WIN_PARENT_PYTHON_HOME` | Windows | `C:\APPLICATIONS\python-3.12.8` |
   | `WIN_PARENT_PYTHON_EXE` | Windows | `python.exe` |
   | `CA_BUNDLE` | Tous *(optionnel)* | `conf/ca_bundle.pem` |

   `CA_BUNDLE` sert derrière un proxy d'inspection SSL (type Zscaler). Chemin absolu ou relatif à la racine du projet ; à laisser commenté s'il n'y a pas de proxy.

3. **Lancer le script d'initialisation** `project-init` (extension `.sh` ou `.ps1` selon votre système, dans `scripts/shell/` ou `scripts/powershell/`). Il crée l'environnement virtuel Python et installe les dépendances.

---

## ⚙️ Configuration

### `conf/application.yaml`

| Clé | Type | Description |
|-----|------|-------------|
| `feed` | liste | Flux à interroger. Chaque entrée porte un `name` et une `url` ; `/feed/` est ajouté automatiquement à l'URL pour obtenir le flux RSS. |
| `watch_list` | liste | Mots-clés recherchés dans le **titre** des publications (insensible à la casse, voir [comportement](#-comportement-à-connaître)). |
| `exclude` | liste | Identifiants de publications à ignorer (ex. `CERTFR-2024-ALE-009`). |
| `smtp.host` | chaîne | Serveur SMTP. Valeur par défaut : `${SMTP_HOST}`. |
| `smtp.port` | chaîne | Port SMTP. Valeur par défaut : `${SMTP_PORT}`. |
| `smtp.user` | chaîne | Compte d'envoi. Valeur par défaut : `${SMTP_USER}`. |
| `smtp.password` | chaîne | Mot de passe. Valeur par défaut : `${SMTP_PWD}`. |
| `smtp.isTls` | booléen | `True` : active STARTTLS avant l'authentification. |
| `email.enable` | booléen | `True` : active l'envoi d'e-mail (`False` par défaut). |
| `email.from` | chaîne | Adresse de l'expéditeur. |
| `email.to` | liste | Destinataires. |
| `email.subject` | chaîne | Objet du message. |
| `email.body` | chaîne | Corps du message (le log est joint). |

Exemple :

```yaml
feed:
- name: avis
  url: https://www.cert.ssi.gouv.fr/avis
- name: alerte
  url: https://www.cert.ssi.gouv.fr/alerte
- name: menaces_incidents
  url: https://www.cert.ssi.gouv.fr/cti

watch_list: [linux, ubuntu, apple, sap, openssh, openssl, python, spark, prometheus, grafana]

exclude: [CERTFR-2024-ALE-009]

smtp:
    host: "${SMTP_HOST}"
    port: "${SMTP_PORT}"
    user: "${SMTP_USER}"
    password: "${SMTP_PWD}"
    isTls: True

email:
    enable: True
    from: 'veille@mondomaine.fr'
    to: ['equipe-securite@mondomaine.fr']
    subject: "Les dernières publications du CERTFR"
    body: "Voici les dernières publications (avis, alerte et menaces) publiées par le CERTFR"
```

Les placeholders `${VARIABLE}` sont remplacés par la valeur de la variable d'environnement correspondante. Les références internes au fichier (ex. `${smtp.host}`) sont également résolues.

### `.env`

Le fichier `.env` (à la racine du projet) contient les paramètres de connexion SMTP :

```dotenv
SMTP_HOST=smtp.mondomaine.fr
SMTP_PORT=587
SMTP_USER=veille@mondomaine.fr
SMTP_PWD=mot_de_passe
```

| Variable | Description |
|----------|-------------|
| `SMTP_HOST` | Nom d'hôte du serveur SMTP |
| `SMTP_PORT` | Port SMTP (587 pour STARTTLS en général) |
| `SMTP_USER` | Compte utilisé pour l'authentification et comme expéditeur de l'enveloppe |
| `SMTP_PWD` | Mot de passe du compte |

Le `.env` est recherché automatiquement en remontant depuis le dossier courant. Il peut aussi servir à surcharger `HOSTNAME`.

> ⚠️ **Sécurité** : ne commitez jamais de vrais identifiants. Versionnez plutôt un fichier `.env.example` et ajoutez `.env` au `.gitignore`.

---

## ▶️ Utilisation

### En programme Python

Depuis `scripts/powershell` (Windows) ou `scripts/shell` (Linux / macOS), lancez le script `app-start` avec le nom du programme :

```powershell
# Windows
cd <APPLICATION_HOME>\scripts\powershell
.\app-start.ps1 surveillance_certfr.py
```

```bash
# Linux / macOS
cd <APPLICATION_HOME>/scripts/shell
./app-start.sh surveillance_certfr.py
```

### Depuis Jupyter ou votre IDE

Ouvrez `notebooks/surveillance_certfr.ipynb` avec l'environnement virtuel créé à l'installation. Le programme `app/surveillance_certfr.py` est la version convertie du notebook :

```powershell
cd <APPLICATION_HOME>\scripts\powershell
.\notebook-converter.ps1 surveillance_certfr.ipynb
```

> **VS Code** : si l'environnement virtuel n'est pas détecté, renseignez `python.defaultInterpreterPath` dans les paramètres.

### Exécution planifiée

L'outil est conçu pour tourner périodiquement. Planifiez simplement `app-start` avec le planificateur de tâches Windows ou avec `cron` (par exemple une fois par jour).

---

## 🔍 Fonctionnement

1. **Initialisation** : le programme remonte l'arborescence jusqu'à trouver `lib/bootstrap/bootstrap.py` pour déterminer la racine (`APPLICATION_HOME`), puis charge le contexte EssencePy (environnement, `.env`, configuration, logger).
2. **Lecture des flux** : pour chaque entrée de `feed`, le flux RSS (`<url>/feed/`) est téléchargé avec `feedparser`.
3. **Filtrage** : une publication est retenue si son titre (en minuscules) contient au moins un mot de `watch_list`.
4. **Journalisation** : les publications retenues sont écrites dans le log (titre, identifiant, lien).
5. **Alerte e-mail** : si au moins une publication correspond **et** que `email.enable` vaut `True`, un message est envoyé via SMTP avec le fichier de log en pièce jointe.

### Logs

- Dossier : `log/` (créé automatiquement).
- Fichier : `surveillance_certfr_AAAA-MM-JJ.log`.
- Rotation à 5 Mo, avec 3 fichiers de sauvegarde conservés.
- Sortie simultanée dans la console.

---

## ⚠️ Comportement à connaître

- **Pas de mémoire des exécutions précédentes** : chaque lancement parcourt le contenu actuel des flux. Une publication encore présente dans le flux sera donc signalée à chaque exécution.
- **Correspondance par sous-chaîne** : un mot-clé court peut matcher à l'intérieur d'un autre mot (ex. `sap` dans un titre contenant « sapin »). Utilisez des mots-clés suffisamment précis et en **minuscules**.
- **Filtrage sur le titre uniquement** : la description des publications n'est pas analysée.
- **`exclude`** : le paramètre est lu depuis la configuration, mais n'est pas encore appliqué lors du filtrage.
- **E-mail** : l'envoi n'est déclenché que si `email.enable` est à `True` ; sinon un avertissement « Sending email alert is OFF » est écrit dans le log.

---

## 🖥️ Environnements de référence

- Windows 10 · PowerShell 5.1 · Python 3.12.8
- Linux · Bash · Python 3.12+
- macOS · Zsh · Python (installé via Homebrew ou python.org)

---

## 📣 À propos

WatchCERTFR est un projet personnel de veille sécurité, bâti sur EssencePy. Les contributions et forks sont les bienvenus.

Les publications surveillées sont la propriété du CERT-FR / ANSSI. Ce projet n'est pas affilié à l'ANSSI.