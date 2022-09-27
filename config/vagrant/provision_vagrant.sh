#!/bin/bash

set -e

apt update
apt -y upgrade

timedatectl set-timezone America/New_York

# Install Python
apt -y install python3 python3-pip
pip3 install -U virtualenv virtualenvwrapper

# Install Docker
apt -y install docker.io
systemctl enable docker containerd
systemctl start docker containerd
usermod -aG docker vagrant

# PostgreSQL
apt -y install postgresql postgresql-contrib libpq-dev

sqlcmd(){
    sudo -u postgres psql -U postgres -d postgres -c "$@"
}
sqlcmd "CREATE DATABASE site_xwords;" || echo Database already exists
sqlcmd "CREATE USER site_xwords PASSWORD 'pwd';" || echo Database user already exists
sed -Ei "s/(^local +all +all +)peer$/\1md5/g" /etc/postgresql/10/main/pg_hba.conf
service postgresql restart

cd xwords

virtualenv -p "$(command -v python3)" --always-copy venv
source ./venv/bin/activate
pip install -r requirements.txt
cp -n xwords/settings/secret.sample.py xwords/settings/secret.py

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
