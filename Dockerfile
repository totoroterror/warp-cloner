FROM python:3.11-alpine

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "src/main.py"]
