# xwords
This site is used to play American-style crossword puzzles in multiple languages

## Developing

CSVs [here](https://drive.google.com/drive/folders/1JIzNG-ygk-ZZ2FMaXsfh4-j_2qim-ZOI?usp=sharing)

This project uses `Vagrant` to standardize development environments

Download `Vagrant` [here](https://www.vagrantup.com/downloads.html)

To run `vagrant` you need two things:
1. Virtualization enabled on your CPU (Intel VT-d, etc.)
  * Google how to do this
2. Oracle VirtualBox installed on your machine
  * Available [here](https://www.virtualbox.org/wiki/Downloads)

After these are installed follow these instructions to get started:

**Important**: Windows Users MUST disable Hyper-V support before continuing
1. Open a command line window and navigate to the directory with the `Vagrantfile`
2. Run `vagrant up`
3. Wait until the VM is finished provisioning
4. Run `vagrant ssh`
5. You are now `ssh`ed into the Vagrant VM!

Starting the Django Server in Vagrant
1. `cd xwords`
2. `source venv/bin/activate`
3. `python3 manage.py runserver 0.0.0.0:8080 --nostatic`
4. Open `localhost:8080` in a web browser on your local machine

### Useful Vagrant commands
Creating superuser for django db:
`python3 manage.py createsuperuser`

Updating psql databse (make sure you have the csv files downloaded):
```
psql -U site_xwords
\copy crosswords_dictionary FROM dictionary.csv DELIMITER ',' CSV
\copy crosswords_word FROM word.csv DELIMITER ',' CSV;
\copy crosswords_definition FROM def.csv DELIMITER ',' CSV;
```

Running celery async process:
`celery --app=xwords worker --loglevel=INFO`

Purging all celery processes:
`celery -A xwords purge`

Note: When running these celery commands you must be in the xwords/ directory

Migration commands:
```
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
```

RabbitMQ commands:
```
apt -y install rabbitmq-server
rabbitmqctl add_user xwords xwords
rabbitmqctl add_vhost xwords
rabbitmqctl add_vhost xwords-celery
rabbitmqctl set_permissions -p xwords xwords ".*" ".*" ".*"
rabbitmqctl set_permissions -p xwords-celery xwords ".*" ".*" ".*"
service rabbitmq-server restart
```

