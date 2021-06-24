FROM python:3.8-alpine as base

FROM base as builder
COPY requirements.txt ./

RUN apk update && apk add build-base && \
pip3 install virtualenv==20.0.33 && \
virtualenv -p /usr/local/bin/python3.8 /venv --always-copy && \
/venv/bin/pip3 install -r requirements.txt

COPY ./ /usr/src/app

FROM base

COPY --from=builder /venv /venv
COPY --from=builder /usr/src/app /usr/src/app
RUN apk add --no-cache tzdata && \
apk del --no-cache --purge .build-deps && \
rm -rf /var/cache/apk/*

WORKDIR /usr/src/app

CMD ["/venv/bin/python3.8", "bot.py"]