
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import requests
import logging
import time
import datetime
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from socket import error as socket_error
import sys
import configparser

# Config msg log
logging.basicConfig(
    filename="display.log", encoding="utf-8", level=logging.ERROR, format="%(asctime)s: %(levelname)s: %(message)s"
)

parser = configparser.ConfigParser()
parser.read("config.txt")

#screen size
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 32

ERROR_CODES = {
    "Connection problem": "ERR 01",
    "No response": "ERR 02"
    }

# small font to display block time
font_time = ImageFont.load_default()
# big font to display block number or err code
font_block = ImageFont.truetype("fonts/DSEG7Classic-Bold.ttf", size=20)
font_err  = ImageFont.truetype("fonts/DSEG14Classic-Bold.ttf", size=20)

def clear():
    disp.fill(0)
    disp.show()

#initialize screen driver
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)
clear()

def blink(seconds):
    image = Image.new('1', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    draw = ImageDraw.Draw(image)

    draw.text((14, 12), "NEW BLK", font=font_err, fill=255)
    for i in range(seconds):
        if i%2:
            disp.image(image)
            disp.show()
            time.sleep(1)
        else:
            clear()
            time.sleep(1)
    
def draw(block, blocktime):
    image = Image.new('1', (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    draw = ImageDraw.Draw(image)

    #  Escribe 2 lineas texto
    draw.text((50, 1),   blocktime,  font=font_time, fill=255)
    draw.text((14, 12), block, font=font_block, fill=255)

    disp.image(image)
    disp.show()
    
def draw_err(err_code):
    image = Image.new('1', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    draw = ImageDraw.Draw(image)

    draw.text((14, 12), block, font=font_err, fill=255)

    disp.image(image)
    disp.show()
    
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = parser.get("config", "rpc_user")
rpc_pass = parser.get("config", "rpc_pass")
rpc_host = parser.get("config", "rpc_host") # if running locally then 127.0.0.1

try:
    rpc_client = AuthServiceProxy(f"http://{rpc_user}:{rpc_pass}@{rpc_host}:8332", timeout=240)
except socket_error as e:
    draw_err(ERROR_CODES["Connection problem"])
    logging.error("Cannot connect to node")
    sys.exit()
    
prev_data = rpc_client.getblockchaininfo()['blocks'] - 1
prev_hash = rpc_client.getblockhash(prev_data)
prev_block = rpc_client.getblock(prev_hash)
prev_time = prev_block['time']

while True:
    data = rpc_client.getblockchaininfo()['blocks']
    hash = rpc_client.getblockhash(data)
    if isinstance(data, int):
        if data != prev_data:
            blink(6)
            prev_data = data
            hash = rpc_client.getblockhash(data)
            block = rpc_client.getblock(hash)
            current_time = block['time']
            elapsed = current_time - prev_time
            elapsed = datetime.timedelta(seconds=elapsed)
            draw(str(data), str(elapsed))
            prev_time = current_time
    else:
        draw_err(ERROR_CODES["No response"])
        logging.error("No response from node")
    time.sleep(20)
