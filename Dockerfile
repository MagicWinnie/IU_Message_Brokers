FROM python:3.12-bullseye as python-base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

WORKDIR /app/src

FROM python-base as api
CMD ["uvicorn", "services.api.service:app",  "--host", "0.0.0.0", "--port", "8000"]

FROM python-base as filter
CMD ["python", "-m", "services.filter.service"]

FROM python-base as screaming
CMD ["python", "-m", "services.screaming.service"]