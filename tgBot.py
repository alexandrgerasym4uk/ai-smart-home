import os
import telebot
import json
import speech_recognition as sr
from pydub import AudioSegment
from core import translate_command

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

TOKEN = config["TG_TOKEN"]
ALLOWED_USERS = config["ALLOWED_USERS"]

bot = telebot.TeleBot(TOKEN)
recognizer = sr.Recognizer()


def format_status(data):
    text = "📊 *СТАН СИСТЕМИ*\n\n"

    text += "💡 Освітлення:\n"
    for room, value in data["lighting"].items():
        state = "увімкнено" if value else "вимкнено"
        text += f"  • {room}: {state}\n"

    vacuum = data["vacuum"]
    text += "\n🤖 Пилосос:\n"
    text += f"  • Стан: {vacuum['state']}\n"
    text += f"  • Потужність: {vacuum['fan_power']}\n"
    text += f"  • Вода: {vacuum['water_level']}\n"

    text += f"\n🌬 Вентиляція: {'увімкнена' if data['ventilation'] else 'вимкнена'}\n"

    climate = data["climate"]
    text += "\n🌡 Клімат:\n"
    text += f"  • Стан: {'увімкнений' if climate['state'] else 'вимкнений'}\n"
    text += f"  • Потужність: {climate['power']}\n"

    ac = data["ac"]
    text += "\n❄️ Кондиціонер:\n"
    text += f"  • Стан: {'увімкнений' if ac['is_on'] else 'вимкнений'}\n"
    text += f"  • Температура: {ac['temperature']}°C\n"
    text += f"  • Режим: {ac['mode']}\n"
    text += f"  • Швидкість: {ac['fan_speed']}\n"
    text += f"  • Swing: {ac['swing']}\n"

    return text


def get_status():
    with open('state.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def is_allowed(message):
    return message.from_user.id in ALLOWED_USERS


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    if is_allowed(message):
        bot.reply_to(message, f"Привіт, {user_name}! \nТвій Telegram ID: `{user_id}`\nЯ готовий. Затисни мікрофон!")
    else:
        bot.reply_to(message, f"Привіт, {user_name}.\nДоступ обмежено.\nТвій Telegram ID: `{user_id}`.")


@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    if not is_allowed(message):
        bot.reply_to(message, "У вас немає доступу.")
        return

    ogg_filename = f"voice_{message.message_id}.ogg"
    wav_filename = f"voice_{message.message_id}.wav"

    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(ogg_filename, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        audio = AudioSegment.from_ogg(ogg_filename)
        audio.export(wav_filename, format="wav")
        
        with sr.AudioFile(wav_filename) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="uk-UA").lower()
            
        print(f"[{message.from_user.first_name}]: {text}")
        bot.reply_to(message, "Виконано")
        
        
        if "стату" in text:
            data = get_status()
            status_text = format_status(data)
            bot.reply_to(message, status_text, parse_mode="Markdown")
            return

        translate_command(text)
        
            
    except sr.UnknownValueError:
        bot.reply_to(message, "Не зміг розібрати слова.")
    except Exception as e:
        bot.reply_to(message, f"Помилка: {str(e)}")
    finally:
        if os.path.exists(ogg_filename):
            os.remove(ogg_filename)
        if os.path.exists(wav_filename):
            os.remove(wav_filename)

@bot.message_handler(commands=['status'])
def send_status(message):
    if not is_allowed(message):
        bot.reply_to(message, "У вас немає доступу.")
        return

    try:
        data = get_status()
        text = format_status(data)
        bot.reply_to(message, text, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"Помилка: {str(e)}")

print("Бот запущений...")
bot.polling(none_stop=True)