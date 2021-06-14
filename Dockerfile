FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

ENV API_KEY_FIREBASE=AIzaSyAaucGQDneM0f-AKbNTKgpcRNzW05wjbyM

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
