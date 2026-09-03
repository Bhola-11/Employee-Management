FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.lock /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py migrate --noinput
RUN python manage.py seed_hrms_data

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
