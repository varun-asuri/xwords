#!/bin/bash
chmod 777 -R public
source venv/bin/activate
daphne -b 127.0.0.1 -p "$PORT" xwords.asgi:application

