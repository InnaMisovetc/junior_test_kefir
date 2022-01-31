# Python and Linux Version
FROM python:3.8.12

COPY requirements.txt /app/requirements.txt

# Configure server
RUN set -ex \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Working directory
WORKDIR /app

ADD . .

#EXPOSE 8000

#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "junior_test_kefir.wsgi:application"]

CMD gunicorn junior_test_kefir.wsgi:application --bind 0.0.0.0:$PORT
