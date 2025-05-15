# --- FRONTEND ---
FROM node:18 AS front
WORKDIR /app
COPY frontend/ .
RUN npm install && npm run build

# --- BACKEND ---
FROM python:3.12-bookworm
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
COPY --from=front /app/dist /app/static
COPY certs/ /app/certs
EXPOSE 8000
CMD ["gunicorn", "burza_project.wsgi:application",
     "--bind", "0.0.0.0:8000",
     "--keyfile", "certs/server.key", "--certfile", "certs/server.crt"]
