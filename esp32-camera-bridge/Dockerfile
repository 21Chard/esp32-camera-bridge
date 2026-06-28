FROM ghcr.io/home-assistant/base:latest

LABEL \
    io.hass.version="1.0.0" \
    io.hass.type="app" \
    io.hass.arch="amd64" \
    org.opencontainers.image.title="ESP32 Camera Bridge" \
    org.opencontainers.image.description="ESP32-CAM MJPEG to RGB565 bridge"

RUN apk add --no-cache \
    python3 \
    py3-pip

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --break-system-packages --no-cache-dir \
    -r /tmp/requirements.txt

COPY server.py /app/server.py
COPY run.sh /run.sh

RUN chmod +x /run.sh

EXPOSE 8088

CMD ["/run.sh"]
