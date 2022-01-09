import configparser

import telebot

import northern_lights_forecast.img as img
import northern_lights_forecast.image_analysis as ima

config = configparser.ConfigParser()
config.read("config.ini")
TOKEN = config["TELEBOT"]["token"]
# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot(TOKEN)  # , parse_mode=None)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Oh hi! Welcome to the nlf interaction bot. I'm able to respond to "
        + "/locations and any message that starts with 'forecast'.",
    )


@bot.message_handler(commands=["locations"])
def send_locations(message):
    txt = "All nlf locations:\n\n"
    for loc in img.__PLACE__.keys():
        txt += f"{loc}\n"
    bot.send_message(message.chat.id, txt)


def is_forecast(message):
    words = message.text.split()
    if words[0].lower() == "forecast" and len(words) > 1:
        return True
    bot.send_message(message.chat.id, "Did you misspell 'forecast'?")
    return False


@bot.message_handler(func=is_forecast)
def get_location_forecast(message):
    """Run the Northern Lights Forecast."""
    words = message.text.split()[1:]
    # check if any of the words are valid locations
    location = "None"
    for w in words:
        for place in img.__PLACE__.keys():
            if w.lower() == place.lower():
                location = place
    if location == "None":
        # Send message that you did it wrong
        bot.send_message(
            message.chat.id,
            f"None of {words} are valid location(s). Type /locations to "
            + "get a complete list of all locations.",
        )
        return

    bot.send_message(
        message.chat.id,
        f"Checking the magnetometer near {location} from the past ~3 hours...",
    )
    scaling = img.img_analysis(location)
    dy = ima.grab_blue_line(scaling)
    txt = (
        f"The gradient in {location} is now at {dy}.\n\n"
        + "Usually, less than -0.5 is okay, less than -1 is good "
        + "and less than -2 is get the fuck out right now!"
    )
    bot.send_message(message.chat.id, txt)


bot.infinity_polling()
