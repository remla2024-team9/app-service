FROM python:3.10-slim

COPY . .

RUN apt-get update && apt-get install -y git

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]