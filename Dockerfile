FROM python:3.13-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements_baseline.txt .
COPY requirements.txt .
RUN pip install -r requirements_baseline.txt
RUN pip install -r requirements.txt

# copy everything
COPY . .

EXPOSE 8001

CMD ["python", "flask-app.py"]

