from flask import Flask, Response
from threading import Thread, Lock
from PIL import Image
import requests
import io
import time

app = Flask(__name__)

# ==========================================================
# Configuration
# ==========================================================

CAMERA_URL = "http://192.168.100.13:8080"

DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 640

# ==========================================================
# Shared Buffers
# ==========================================================

latest_jpeg = None
latest_rgb565 = None

frame_lock = Lock()

fps = 0
frame_counter = 0
last_time = time.time()


def image_to_rgb565(img):

    img = img.convert("RGB")
    pixels = img.load()

    buffer = bytearray()

    for y in range(img.height):
        for x in range(img.width):

            r, g, b = pixels[x, y]

            rgb565 = (
                ((r & 0xF8) << 8) |
                ((g & 0xFC) << 3) |
                (b >> 3)
            )

            buffer.append((rgb565 >> 8) & 0xFF)
            buffer.append(rgb565 & 0xFF)

    return bytes(buffer)


def camera_thread():

    global latest_jpeg
    global latest_rgb565
    global frame_counter
    global fps
    global last_time

    while True:

        try:

            print("Connecting to camera...")

            stream = requests.get(
                CAMERA_URL,
                stream=True,
                timeout=10
            )

            bytes_buffer = b''

            for chunk in stream.iter_content(1024):

                bytes_buffer += chunk

                start = bytes_buffer.find(b'\xff\xd8')
                end = bytes_buffer.find(b'\xff\xd9')

                if start != -1 and end != -1:

                    jpg = bytes_buffer[start:end+2]
                    bytes_buffer = bytes_buffer[end+2:]

                    image = Image.open(io.BytesIO(jpg))

                    image = image.resize(
                        (DISPLAY_WIDTH, DISPLAY_HEIGHT),
                        Image.Resampling.BILINEAR
                    )

                    rgb565 = image_to_rgb565(image)

                    with frame_lock:
                        latest_jpeg = jpg
                        latest_rgb565 = rgb565

                    frame_counter += 1

                    now = time.time()

                    if now - last_time >= 1:

                        fps = frame_counter

                        frame_counter = 0
                        last_time = now

        except Exception as e:

            print(e)

            print("Reconnect in 2 seconds")

            time.sleep(2)


# ==========================================================
# Flask Endpoints
# ==========================================================

@app.route("/")
def index():
    return """
    <html>
    <head><title>ESP32 Camera Bridge</title></head>
    <body>
    <h2>ESP32 Camera Bridge Running</h2>
    <ul>
        <li><a href="/status">/status</a></li>
        <li><a href="/fps">/fps</a></li>
        <li><a href="/preview.jpg">/preview.jpg</a></li>
        <li><a href="/frame565">/frame565</a></li>
    </ul>
    </body>
    </html>
    """


@app.route("/status")
def status():

    with frame_lock:
        ready = latest_rgb565 is not None

    return {
        "status": "running",
        "camera": CAMERA_URL,
        "frame_ready": ready,
        "width": DISPLAY_WIDTH,
        "height": DISPLAY_HEIGHT,
        "fps": fps
    }


@app.route("/fps")
def fps_endpoint():
    return str(fps)


@app.route("/preview.jpg")
def preview():

    with frame_lock:
        if latest_jpeg is None:
            return Response("No frame available", status=503)

        data = latest_jpeg

    return Response(
        data,
        mimetype="image/jpeg"
    )


@app.route("/frame565")
def frame565():

    with frame_lock:

        if latest_rgb565 is None:
            return Response("No frame available", status=503)

        frame = latest_rgb565

    return Response(
        frame,
        mimetype="application/octet-stream",
        headers={
            "Content-Length": str(len(frame)),
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Origin": "*"
        }
    )


@app.route("/info")
def info():

    with frame_lock:
        size = len(latest_rgb565) if latest_rgb565 else 0

    return {
        "display": f"{DISPLAY_WIDTH}x{DISPLAY_HEIGHT}",
        "rgb565_size": size,
        "expected": DISPLAY_WIDTH * DISPLAY_HEIGHT * 2,
        "camera": CAMERA_URL,
        "fps": fps
    }

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("========================================")
    print("ESP32 Camera Bridge Starting...")
    print("Camera:", CAMERA_URL)
    print("========================================")

    Thread(
        target=camera_thread,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=8088,
        threaded=True,
        debug=False
    )
