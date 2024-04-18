

# Movie Recommender System

This project demonstrates basic backend CRUD operations, token authentication, role based access and movie recommendation utility which uses, KNN algorithm.

## Run Locally

Create virtual environment

```bash
  virtualenv venv
```

Activate virtual environment

```bash
  .\venv\Scripts\activate
```

Clone the project

```bash
  git clone https://github.com/krish-patel1003/recommender_system
```

Go to the project directory

```bash
  cd recommender_system
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py collectstatic
  python manage.py runserver
```


