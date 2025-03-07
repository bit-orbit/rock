#!/usr/bin/env python

import telebot
import os
import sys
import time
import threading

# Get the bot token from the environment variable
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

DOWNLOAD_FOLDER = "./raw"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

last_message_time = time.time()
inactivity_timeout = 60  # seconds of inactivity before exit

message_received = threading.Event() # thread safe flag

@bot.message_handler(content_types=['document', 'video', 'audio', 'voice'])
def handle_files(message):
    global last_message_time
    last_message_time = time.time()  # Update the last message time
    message_received.set() # set the message received flag
    try:
        file_info = None
        file_name = None

        if message.document:
            file_info = bot.get_file(message.document.file_id)
            file_name = message.document.file_name
        elif message.video:
            file_info = bot.get_file(message.video.file_id)
            file_name = message.video.file_name
        elif message.audio:
            file_info = bot.get_file(message.audio.file_id)
            file_name = message.audio.file_name
        elif message.voice:
            file_info = bot.get_file(message.voice.file_id)
            file_name = f"voice_{message.voice.file_id}.ogg"

        if file_info and file_name:
            downloaded_file = bot.download_file(file_info.file_path)
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, f"File '{file_name}' downloaded successfully!")
        else:
            bot.reply_to(message, "Failed to download the file.")

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

def check_inactivity():
    global last_message_time
    if time.time() - last_message_time > inactivity_timeout:
        print("Inactivity timeout. Exiting...")
        sys.exit(0)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send me a file, and I'll download it!")

print("Bot started. Listening for files...")

def run_polling():
    while True:
        try:
            bot.polling(none_stop=False, interval=1)
        except Exception as e:
            print(f"Error during polling: {e}")
            time.sleep(5)

polling_thread = threading.Thread(target=run_polling)
polling_thread.daemon = True # allow the main thread to exit even if this thread is running
polling_thread.start()

while True:
    message_received.wait(1) # wait for one second, or until a message is received.
    if message_received.is_set():
        message_received.clear()
    check_inactivity()