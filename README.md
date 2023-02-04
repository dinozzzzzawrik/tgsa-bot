**Telegram Steam Guard**

=================
Table of contents
=================

- `Introduction`

- `Installing`

- `Getting help`

- `Contributing`

- `How to add account in db`

============
Introduction
============

This is one of TGSA project part - Telegram BOT  

==========
Installing
==========

    $ git clone https://github.com/dinozzzzzawrik/tgsa-bot.git
    
    Setup envs:
    
    - Create .env file with BOT_TOKEN=token here in it
    
    $ pip install -r requirements.txt
    $ python run.py

============
Getting help
============

You can get help using issues:

Report bugs, request new features or ask questions by `creating an issue`

============
Contributing
============

Contributions of all sizes are welcome

======================================================
How to add account in db - will make it by admin panel
======================================================

Open python shell

    $ from models import *


    $ account = Accounts(name='account name in db', key='shared_secret valie from Mafile')
    $ account.save()

    $ user = WhiteList(name='User name', tg_id=telegram id from @userinfobot)
    $ user.save()
