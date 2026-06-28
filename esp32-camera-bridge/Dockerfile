FROM ghcr.io/home-assistant/base:latest

LABEL \
  io.hass.version="1.0.5" \
  io.hass.type="app" \
  io.hass.arch="amd64"

RUN apk add --no-cache \
    python3 \
    py3-pip \
    build-base \
    jpeg-dev \
    zlib-dev

COPY requirements.txt /requirements.txt

RUN python3 -m pip install --no-cache-dir --break-system-packages -r /requirements.txt

RUN python3 -m pip list

COPY server.py /server.py
COPY run.sh /run.sh

RUN chmod +x /run.sh

EXPOSE 8088

CMD ["/run.sh"]
