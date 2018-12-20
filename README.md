
## Introduction

Suit l'avancement des procédures devant le juge administratif en cherchant l'information sur le portail SAGACE. En cas de changement, envoie un mail.

## Install

Use python3 (it may work for python2).

```
pew new ping-sagace
pip install -r requirements.txt
```

Copy `credentials.json.example` to `credentials.json`.

Copy `mail_config.json.example` to `mail_config.json`.

Add to `/etc/crontab` something like: `45 19	* * *	myuser	/home/myuser/.local/share/virtualenvs/ping-sagace/bin/python /home/myuser/ping-sagace/src/run.py`
