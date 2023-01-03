import mimetypes
from flask import Flask, send_file, abort, Response, redirect, make_response, request
from PIL import Image, ImageDraw, ImageFont
import random
import json
from io import BytesIO
import time
from datetime import datetime


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


@app.route('/bash/start')
def start_bash():
    # Load game data from bashData.json
    with open('bashData.json', 'r') as f:
        games = json.load(f)

    # Delete any games that have existed for more than 10 minutes
    current_time = time.time()
    codes_to_delete = []
    for code, game in games["games"].items():
        if current_time - game["timestamp"] > 10 * 60:
            codes_to_delete.append(code)
    for code in codes_to_delete:
        del games["games"][code]

    # Generate random 5-digit code
    code = ''.join(str(random.randint(0, 9)) for _ in range(5))
    while code in games:  # Make sure code is not already in use
        code = ''.join(str(random.randint(0, 9)) for _ in range(5))

    # Create new game data in the format you've described
    game_data = {
        "player1": {
            "ships": [],
            "hits": [],
            "remaining": "5"
        },
        "player2": {
            "ships": [],
            "hits": [],
            "remaining": "5"
        },
        "turn": "1"
    }
    game_data["timestamp"] = time.time()  # Add timestamp to game data

    # Generate ship positions for player1 and player2
    for player in ["player1", "player2"]:
        ships = []
        # Generate ship positions for each ship size
        for size in [5, 4, 3, 3, 2]:
            while True:  # Keep trying until ship position is generated successfully
                # Generate random ship position (random orientation and random starting position)
                orientation = random.choice(["horizontal", "vertical"])
                if orientation == "horizontal":
                    x = random.randint(0, 9 - size)
                    y = random.randint(0, 9)
                    coordinates = [f"{chr(ord('A') + x + i)}{y}" for i in range(size)]
                else:
                    x = random.randint(0, 9)
                    y = random.randint(0, 9 - size)
                    coordinates = [f"{chr(ord('A') + x)}{y + i}" for i in range(size)]

                # Check if generated ship position overlaps with any existing ship positions
                overlaps = False
                for ship in ships:
                    if any(coord in ship["coordinates"] for coord in coordinates):
                        overlaps = True
                        break
                if not overlaps:
                    break  # Ship position does not overlap, break out of loop

            ships.append({
                "size": size,
                "coordinates": coordinates
            })
            game_data[player]["ships"] = ships

    games["games"][code] = game_data
    with open('bashData.json', 'w') as f:
        json.dump(games, f)

    # Load start.png and draw code on top of it
    img = Image.open('start.png')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 36)
    draw.text((170, 452), f"https://verumignis.com/bash/{code}2/st.png", font=font, fill=(255, 255, 255))

    # Save modified image to memory
    with BytesIO() as buffer:
        img.save(buffer, 'PNG')
        buffer.seek(0)
        img_data = buffer.read()

    # Return image in response
    response = make_response(img_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/bash/<game_code>/st.png')
def bash_st(game_code):
    # Load game data from bashData.json
    with open('bashData.json', 'r') as f:
        games = json.load(f)

    # Delete any games that have existed for more than 10 minutes
    current_time = time.time()
    codes_to_delete = []
    for code, game in games["games"].items():
        if current_time - game["timestamp"] > 10 * 60:
            codes_to_delete.append(code)
        else:
            # set the timestamp to the current time
            game["timestamp"] = current_time
    for code in codes_to_delete:
        del games["games"][code]

    with open('bashData.json', 'w') as f:
        json.dump(games, f)

    # Check if game code is valid
    if game_code[:-1] not in games["games"]:
        # Return error2.png
        with open('error2.png', 'rb') as f:
            img_data = f.read()
        response = make_response(img_data)
        response.headers['Content-Type'] = 'image/png'
        return response

    # Check last character of game code
    if game_code[-1] == '1':
        # Return continue.png
        with open('continue.png', 'rb') as f:
            img_data = f.read()
        response = make_response(img_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    elif game_code[-1] == '2':
        # Load handshake.png and draw game code and link on top of it
        img = Image.open('handshake.png')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 36)
        draw.text((450, 237), f"{game_code[:-1]}2", font=font, fill=(255, 255, 255))
        draw.text((170, 452), f"https://verumignis.com/bash/{game_code[:-1]}1/st.png", font=font, fill=(255, 255, 255))

        # Save modified image to memory
        with BytesIO() as buffer:
            img.save(buffer, 'PNG')
            buffer.seek(0)
            img_data = buffer.read()

        # Return image in response
        response = make_response(img_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    else:
        # Return error1.png
        with open('error2.png', 'rb') as f:
            img_data = f.read()
        response = make_response(img_data)
        response.headers['Content-Type'] = 'image/png'
        return response

@app.route('/bash/<game_code>/rl.png')
def bash_rules(game_code):
    # Load game data from bashData.json
    with open('bashData.json', 'r') as f:
        games = json.load(f)

    # Delete any games that have existed for more than 10 minutes
    current_time = time.time()
    codes_to_delete = []
    for code, game in games["games"].items():
        if current_time - game["timestamp"] > 10 * 60:
            codes_to_delete.append(code)
        else:
            # set the timestamp to the current time
            game["timestamp"] = current_time
    for code in codes_to_delete:
        del games["games"][code]

    with open('bashData.json', 'w') as f:
        json.dump(games, f)

    # Check if game code is valid
    if game_code[-1] == "1" or game_code[-1] == "2":
        if game_code[:-1] in games["games"]:
            with open('rules.png', 'rb') as f:
                img_data = f.read()
            response = make_response(img_data)
            response.headers['Content-Type'] = 'image/png'
            return response
        else:
            with open('error2.png', 'rb') as f:
                img_data = f.read()
            response = make_response(img_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        with open('error2.png', 'rb') as f:
            img_data = f.read()
        response = make_response(img_data)
        response.headers['Content-Type'] = 'image/png'
        return response

@app.route('/bash/<game_code>/<command>.png')
def bash_game(game_code, command):
    is_hit = False
    # Load game data from bashData.json
    with open('bashData.json', 'r') as f:
        games = json.load(f)

    turn = games["games"][game_code[:-1]]["turn"]
    hits = games["games"][game_code[:-1]][f"player{game_code[-1]}"]["hits"]
    remaining = games["games"][game_code[:-1]][f"player{game_code[-1]}"]["remaining"]
    if game_code[-1] == "1":
        opHits = games["games"][game_code[:-1]]["player2"]["hits"]
        op_ships = games["games"][game_code[:-1]]["player2"]["ships"]
        opRemaining = games["games"][game_code[:-1]]["player2"]["remaining"]
    else:
        opHits = games["games"][game_code[:-1]]["player1"]["hits"]
        op_ships = games["games"][game_code[:-1]]["player1"]["ships"]
        opRemaining = games["games"][game_code[:-1]]["player1"]["remaining"]

    if opRemaining == "0":
        with open('win.png', 'rb') as f:
            img_data = f.read()
        response = make_response(img_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    elif remaining == "0":
        with open('win.png', 'rb') as f:
            img_data = f.read()
        response = make_response(img_data)
        response.headers['Content-Type'] = 'image/png'
        return response

    if turn == game_code[-1] or command == "rd":
        if isinstance(command, str) and len(command) == 2 and command[0].isalpha() and command[1].isdigit() and command not in hits or command == "rd":
            if not command == "rd":
                if turn == "1":
                    turn = "2"
                else:
                    turn = "1"
                games["games"][game_code[:-1]][f"player{game_code[-1]}"]["hits"].append(command)

                for ship in op_ships:
                    if command in ship["coordinates"]:
                        is_hit = True
                        break
                op_ships_remaining = 0
                for ship in op_ships:
                    if not set(ship["coordinates"]).issubset(set(opHits)):
                        op_ships_remaining += 1
                opRemaining = op_ships_remaining
                games["games"][game_code[:-1]]["turn"] = turnv


            current_time = time.time()
            codes_to_delete = []
            for code, game in games["games"].items():
                if current_time - game["timestamp"] > 10 * 60:
                    codes_to_delete.append(code)
                else:
                    game["timestamp"] = current_time
            for code in codes_to_delete:
                del games["games"][code]

            player_ships = []
            if game_code[-1] == '1':
                if game_code[:-1] in games["games"]:
                    player_ships = games["games"][game_code[:-1]]["player1"]["ships"]
                else:
                    with open('error2.png', 'rb') as f:
                        img_data = f.read()
                    response = make_response(img_data)
                    response.headers['Content-Type'] = 'image/png'
                    return response
            elif game_code[-1] == '2':
                if game_code[:-1] in games["games"]:
                    player_ships = games["games"][game_code[:-1]]["player2"]["ships"]
                else:
                    with open('error2.png', 'rb') as f:
                        img_data = f.read()
                    response = make_response(img_data)
                    response.headers['Content-Type'] = 'image/png'
                    return response
            else:
                with open('error2.png', 'rb') as f:
                    img_data = f.read()
                response = make_response(img_data)
                response.headers['Content-Type'] = 'image/png'
                return response

            with open('bashData.json', 'w') as f:
                json.dump(games, f)

            background_img = Image.open('background.png')
            hit_img = Image.open('hit.png')
            draw = ImageDraw.Draw(background_img)
            font = ImageFont.truetype('arial.ttf', 36)
            draw.text((10, 520), f"Type s/{command}/<new position> and press enter.", font=font, fill=(255, 255, 255))
            if not command == "rd":
                if is_hit:
                    draw.text((943, 520), "HIT", font=font, fill=(255, 255, 255))
                else:
                    draw.text((922, 520), "MISS", font=font, fill=(255, 255, 255))

            for ship in player_ships:
                for coord in ship["coordinates"]:
                    x = (ord(coord[0]) - 65) * 44 + 37
                    y = (int(coord[1]) - 1) * 44 + 81
                    draw.rectangle([(x, y), (x + 42, y + 42)], fill='white', outline='black')

            for hit in opHits:
                x = (ord(hit[0]) - 65) * 44 + 37
                y = (int(hit[1]) - 1) * 44 + 81
                background_img.paste(hit_img, (x, y), hit_img)

            for ship in op_ships:
                for coord in ship["coordinates"]:
                    x = (ord(coord[0]) - 65) * 44 + 548
                    y = (int(coord[1]) - 1) * 44 + 81
                    if coord in hits:
                        draw.rectangle([(x, y), (x + 42, y + 42)], fill='white', outline='black')

            for hit in hits:
                x = (ord(hit[0]) - 65) * 44 + 548
                y = (int(hit[1]) - 1) * 44 + 81
                background_img.paste(hit_img, (x, y), hit_img)

            img_bytes = BytesIO()
            background_img.save(img_bytes, 'png')
            img_bytes.seek(0)
            img_data = img_bytes.read()
            response = make_response(img_data)
            response.headers['Content-Type'] = 'image/png'
            return response
        else:
            with open('error1.png', 'rb') as f:
                img_data = f.read()
            response = make_response(img_data)
            response.headers['Content-Type'] = 'image/png'
            return response

    else:
        with open('error3.png', 'rb') as f:
            img_data = f.read()
        response = make_response(img_data)
        response.headers['Content-Type'] = 'image/png'
        return response

@app.route('/bitmapgen/<input_string>')
def bitmapgen(input_string):
    image = Image.new('RGB', (160, 160), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    for y, row in enumerate(input_string.split('-')):
        if "¦" in input_string:
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
    if ".." in filename or "bashData" in filename:
        return "nice try :)"
    elif "duck.webm" in filename or "cool-video" in filename:
        f = open("rickrolls.txt", "r")
        rickrollCount = int(f.read())
        f.close()
        newCount = rickrollCount + 1
        f = open("rickrolls.txt", "w")
        f.write(str(newCount))
        f.close()
    if "cool-video" in filename:
        return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    try:
        mimetype = mimetypes.guess_type(filename)[0]
        return send_file(filename, mimetype=mimetype)
    except FileNotFoundError:
        abort(404)

@app.errorhandler(404)
def not_found(error):
    return send_file("404.html", mimetype="text/html"), 404

@app.errorhandler(500)
def internal_server_error(error):
    if "bash" in request.path:
        with open('error2.png', 'rb') as f:
            img_data = f.read()
        response = make_response(img_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    return send_file("500.html", mimetype="text/html"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')

