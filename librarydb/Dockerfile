FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN python -m pip install Django
RUN pip install django-bootstrap-v5
RUN pip install psycopg2

EXPOSE 8000

ENTRYPOINT [ "python", "manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ] 