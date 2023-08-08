FROM alpine:3.18 AS compile-image

RUN apk update
RUN apk add --no-cache make automake gcc g++ subversion python3-dev libffi-dev

WORKDIR /app

COPY ./requirements.txt /app/
RUN python3 -m venv /app
RUN /app/bin/pip install -r requirements.txt
RUN rm -rf /app/lib/python3.11/site-packages/setuptools* && \
    rm -rf /app/lib/python3.11/site-packages/pip* && \
    rm -rf /app/bin/pip*

FROM alpine:3.18 AS runtime-image

RUN apk add --no-cache python3

WORKDIR /app

COPY . /app

COPY --from=compile-image /app/ ./

CMD ["/app/bin/python3", "src/main.py"]
