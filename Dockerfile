FROM python:3.9-slim-buster

WORKDIR /app
COPY pyproject.toml .

RUN pip install pdm
RUN pdm install --no-lock
CMD ["pdm", "run", "python", "-m", "app"]
