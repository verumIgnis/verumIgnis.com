import mimetypes
from flask import Flask, send_file, abort, Response, redirect
from PIL import Image, ImageDraw

app = Flask(__name__)

base64_to_rgb = {'A': 0, 'B': 4, 'C': 8, 'D': 12, 'E': 16, 'F': 20, 'G': 24, 'H': 28, 'I': 32, 'J': 36, 'K': 40,
                 'L': 44, 'M': 48, 'N': 52, 'O': 56, 'P': 60, 'Q': 64, 'R': 68, 'S': 72, 'T': 76, 'U': 80, 'V': 84,
                 'W': 88, 'X': 92, 'Y': 96, 'Z': 100, 'a': 104, 'b': 108, 'c': 112, 'd': 116, 'e': 120, 'f': 124,
                 'g': 128, 'h': 132, 'i': 136, 'j': 140, 'k': 144, 'l': 148, 'm': 152, 'n': 156, 'o': 160, 'p': 164,
                 'q': 168, 'r': 172, 's': 176, 't': 180, 'u': 184, 'v': 188, 'w': 192, 'x': 196, 'y': 200, 'z': 204,
                 '0': 208, '1': 212, '2': 216, '3': 220, '4': 224, '5': 228, '6': 232, '7': 236, '8': 240, '9': 244,
                 '_': 248, ';': 252, '¬': 255}


def draw_pixel(draw, x, y, color):
    draw.rectangle((x * 10, y * 10, x * 10 + 10, y * 10 + 10), fill=color)


@app.route('/')
def index():
    return send_file("index.html", mimetype="text/html")


@app.route('/cool-video')
def cool_video():
    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


@app.route('/bitmapgen/<input_string>')
def bitmapgen(input_string):
    image = Image.new('RGB', (160, 160), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    for y, row in enumerate(input_string.split('-')):
        if len(row) > 16:
            for x, pixel in enumerate(row.split('¦')):
                bits = list(pixel)
                pixelSplit = (bits[0], bits[1], bits[2])
                r, g, b = map(base64_to_rgb.get, pixelSplit)
                draw_pixel(draw, x, y, (r, g, b))
        else:
            for x, pixel in enumerate(row):
                if pixel == "0":
                    colour = (0, 0, 0)
                elif pixel == "1":
                    colour = (255, 255, 255)
                elif pixel == "2":
                    colour = (255, 0, 0)
                elif pixel == "3":
                    colour = (0, 255, 0)
                elif pixel == "4":
                    colour = (0, 0, 255)
                elif pixel == "5":
                    colour = (255, 255, 0)
                elif pixel == "6":
                    colour = (255, 0, 255)
                elif pixel == "7":
                    colour = (0, 255, 255)
                elif pixel == "8":
                    colour = (255, 128, 0)
                elif pixel == "9":
                    colour = (128, 128, 128)
                else:
                    colour = (0, 0, 0)
                draw_pixel(draw, x, y, colour)

    response = Response(mimetype='image/png')
    image.save(response.stream, format='PNG')
    return response


@app.route('/<path:filename>')
def serve(filename):
    try:
        mimetype = mimetypes.guess_type(filename)[0]
        return send_file(filename, mimetype=mimetype)
    except FileNotFoundError:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    return send_file("404.html", mimetype="text/html"), 404


if __name__ == '__main__':
    app.run()

