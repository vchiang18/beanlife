FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip

WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt

CMD python manage.py migrate && python manage.py runserver "0.0.0.0:8000"


# FROM python:3.10-bullseye
# ENV PYTHONUNBUFFERED 1
# RUN python -m pip install --upgrade pip

# WORKDIR /app

# ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
# RUN chmod +x /wait

# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# #alternative^ below?
# # COPY requirements.txt /app/
# # RUN pip install --no-cache-dir -r requirements.txt

# CMD /wait && python manage.py migrate && python manage.py runserver "0.0.0.0:8000"
