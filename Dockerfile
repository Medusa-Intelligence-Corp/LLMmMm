FROM python:slim

WORKDIR /usr/src/app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    flask \
    flask-cors \
    gunicorn \
    smartenough \
    bleach

COPY . .

# to run this locally you want to change the port to 5000
# to deploy on a server, probably change to port 80
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
