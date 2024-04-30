FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip
RUN python -m pip install python-dotenv

# Install Node.js
RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt

CMD python manage.py migrate && python manage.py runserver "0.0.0.0:8000"
