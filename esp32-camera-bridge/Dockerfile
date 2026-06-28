ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apk add --no-cache python3 py3-pip

COPY requirements.txt /tmp/

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY server.py /app/
COPY run.sh /

RUN chmod +x /run.sh

CMD ["/run.sh"]
