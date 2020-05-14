FROM python:3.8.2-slim-buster

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code/

RUN pip install pipenv

COPY Pipfile* /code/
RUN pipenv install --deploy --ignore-pipfile

ADD ./scraper /code

CMD ["pipenv", "run", "uvicorn", "scraper.main:app", "--host", "0.0.0.0"]
