FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY chroma/ /app/chroma/
COPY . .

RUN pip install --no-cache-dir -e .

CMD ["uvicorn", "app.main:app","--host","0.0.0.0","--port","8080"]
EXPOSE 8080
