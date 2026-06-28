FROM ghcr.io/home-assistant/base:latest

LABEL \
  io.hass.version="1.0.0" \
  io.hass.type="app" \
  io.hass.arch="amd64"

RUN apk add --no-cache \
    python3 \
    py3-pip

COPY run.sh /
COPY server.py /

RUN chmod +x /run.sh

CMD ["/run.sh"]
