#!/usr/bin/env python3

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import logging
import time
import datetime
from bitcoinrpc.authproxy import AuthServiceProxy
from socket import error as socket_error
import sys, os
import configparser


CURRENT_PATH =os.path.dirname(sys.argv[0])
REFRESH_INTERVAL = 20

# Config msg log
logging.basicConfig(
    filename=CURRENT_PATH + "/display.log", encoding="utf-8", level=logging.ERROR, format="%(asctime)s: %(levelname)s: %(message)s"
)

ERROR_CODES = {
    "Connection problem": "ERR 01",
    "No response": "ERR 02"
    }

# read config file
parser = configparser.ConfigParser()
parser.read(CURRENT_PATH + "/config.txt")

rpc_user = parser.get("config", "rpc_user")
rpc_pass = parser.get("config", "rpc_pass")
rpc_host = parser.get("config", "rpc_host") # if running locally then 127.0.0.1

# set screen size
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 32

# small font to display block time
font_time = ImageFont.load_default()
# big font to display block number or err code
font_block = ImageFont.truetype(CURRENT_PATH + "/fonts/DSEG7Classic-Bold.ttf", size=20)
font_err  = ImageFont.truetype(CURRENT_PATH + "/fonts/DSEG14Classic-Bold.ttf", size=20)

def clear():
    disp.fill(0)
    disp.show()

# Initialize screen driver
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)
clear()

# Blinks and show "NEW BLK" for n seconds when a new block is found
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

# Shows block height and block time    
def draw(block, blocktime):
    image = Image.new('1', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.text((50, 1),   blocktime,  font=font_time, fill=255)
    draw.text((14, 12), block, font=font_block, fill=255)
    disp.image(image)
    disp.show()

# Shows error code
def draw_err(err_code):
    image = Image.new('1', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.text((14, 12), err_code, font=font_err, fill=255)
    disp.image(image)
    disp.show()

try:
    rpc_client = AuthServiceProxy(f"http://{rpc_user}:{rpc_pass}@{rpc_host}:8332", timeout=240)
except socket_error as e:
    draw_err(ERROR_CODES["Connection problem"])
    logging.error("Cannot connect to node")
    sys.exit()
    
prev_blk_height = rpc_client.getblockchaininfo()['blocks'] - 1
prev_hash = rpc_client.getblockhash(prev_blk_height)
prev_block = rpc_client.getblock(prev_hash)
prev_time = prev_block['time']

while True:
    current_blk_height = rpc_client.getblockchaininfo()['blocks']
    current_blk_hash = rpc_client.getblockhash(current_blk_height)
    if isinstance(current_blk_height, int):
        if current_blk_height != prev_blk_height:
            blink(6)
            prev_blk_height = current_blk_height
            current_blk_hash = rpc_client.getblockhash(current_blk_height)
            current_block = rpc_client.getblock(current_blk_hash)
            current_time = current_block['time']
            elapsed = current_time - prev_time
            elapsed = datetime.timedelta(seconds=elapsed)
            draw(str(current_blk_height), str(elapsed))
            prev_time = current_time
    else:
        draw_err(ERROR_CODES["No response"])
        logging.error("No response from node")
    time.sleep(REFRESH_INTERVAL)