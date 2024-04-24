FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip
RUN python -m pip install python-dotenv

WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt

CMD python manage.py migrate && python manage.py runserver "0.0.0.0:8000"
