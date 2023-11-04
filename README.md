# API for Personal Blog Project

## Preview :
![Part One Image](static/doc/image/api-part-1.png)
<br>
![Part Two Image](static/doc/image/api-part-2.png)

Backend Setup :
- Python 3.11.4
- FastAPI 0.101.1
- pymysql 1.1.0
- Docker as Database Management (phpmyadmin and mysql) for Development
- Docker for deployment

> Be carefull with python version.
> Always using environment like [anaconda](https://www.anaconda.com/)/[miniconda](https://docs.conda.io/en/latest/miniconda.html)/[virtualenv](https://virtualenv.pypa.io/en/latest/) for setup backend.
> Don't forget to activate environment.

Want to contribute? Great!
## Development

Create python env using miniconda/anaconda

```sh
conda create --name personal-blog-api
```

Activate python env

```sh
conda activate personal-blog-api
```

> Note:  activate environment and set python interpreter to your environment. if using vscode do `ctrl+shift+p` then write `python interpreter`, after that select the right environment
> After select python interpreter, kill terminal in vscode then add terminal to prevent environment still work in global



### Generate Key for Private Key, Public Key, Refresh Private Key

generate private key

```sh
openssl genrsa -out private.pem 2048
```

generate public key

```sh
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```

generate private key for refresh

```sh
openssl genrsa -out private-refresh.pem 2048
```

### Setup database for development

Add database image in docker with phpmyadmin

```sh
docker-compose -f docker-compose.dev.yml up --build -d
```

> Alternate way : just install mysql in your local

### Connect database

Duplicate alembic.ini.example and renamed it to alembic.ini

Duplicate .env.example and renamed it to .env

Fill this variable in .env
```sh
DB="mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
# or default from docker "mysql+pymysql://user:user@localhost:4306/personal_blog_api"
```

### Setup project

Install package

```sh
pip install -r requirements.txt
```

Running migration table

```sh
alembic upgrade head
```

Running Application

```sh
uvicorn main:app --reload
```

Look endpoint list in Swagger Documentation

```sh
http://localhost:8000/docs
```

### Deploy for production

Up docker

```sh
docker-compose up -d --build
```

> Use option --build for first time only or if there a new package

Look endpoint list in local Swagger Documentation (Production)

```sh
http://localhost:8120/docs
```

> Should be restart docker if there area updated code in production
