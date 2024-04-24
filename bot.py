import requests, json, wget
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
# Aiogram parametres

API_TOKEN = '6307067231:AAHYAUDYRl0jfKreCCyYR3LWjtU1KZ7wjUc'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()

def create_user(username,user_id):
    url = f"https://urgaz.pythonanywhere.com/"
    response = requests.get(url=url).text
    data = json.loads(response)
    list = []
    for i in data:
        list.append(i["teleId"])
    if user_id not in list:
        requests.post(url=url, data={"username":username,"teleId":user_id})

# Api parametres
photo_url = "https://urgaz.pythonanywhere.com/"
url = "https://urgaz.pythonanywhere.com/carpets/"

def check_similarity(text1, text2):
    return text1.casefold() == text2.casefold()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    create_user(str(message.from_user.username),str(message.from_user.id))
    # Reply Buttons
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Yangi dizaynlar'))
    keyboard.row(KeyboardButton("Gilamlar"), KeyboardButton('Sun\'iy Gazon'))
    keyboard.row(KeyboardButton('Kontakt'))
    keyboard.add(KeyboardButton('Web Sahifa'))
    await message.reply("Assalomu alaykum! \"Urgaz Carpet\" kompaniyasining rasmiy botiga \n Xush Kelibsiz!!!.", reply_markup=keyboard)

# Reply Yangi dizaynlar
@dp.message_handler(Text('Yangi dizaynlar'))
async def reply_button_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Yangi dizaynlar",request_contact=True, request_location=True, callback_data='disabled'))
    response = requests.get(url=url+"new/")
    if response.status_code == 200:
        datas = json.loads(response.text)
        if len(datas)>1:
            i = int(len(datas))
            for n in range(0, i,2):
                button1 = KeyboardButton(datas[n - 1]['name'])
                button2 = KeyboardButton(datas[n]['name'])
                if button1 and button2  not in keyboard  : 
                    keyboard.row(button1, button2)
                elif button1 in keyboard and button2 not in keyboard:
                    keyboard.row(button2,'')
                elif button2 in keyboard and button1 not in keyboard:
                    keyboard.row(button2,'')
        else:
            button1 = KeyboardButton(datas[0]['name'])
            keyboard.row(button1)
        keyboard.add(KeyboardButton("Go Back"))
    else:
        print(f"Request error: {response.status_code}")
    await message.reply("Yangi Dizaynlar Tanlandi!", reply_markup=keyboard)


@dp.message_handler(Text("Gilamlar"))
async def reply_button_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Gilamlar",request_contact=True, request_location=True, callback_data='disabled'))
    response = requests.get(url=url)
    if response.status_code == 200:
        datas = json.loads(response.content)
        if len(datas)>1:
            i = int(len(datas))
            for n in range(0, i,2):
                button1 = KeyboardButton(datas[n - 1]['carpet'])
                button2 = KeyboardButton(datas[n]['carpet'])
                if button1 and button2  not in keyboard  : 
                    keyboard.row(button1, button2)
                elif button1 in keyboard and button2 not in keyboard:
                    keyboard.row(button2,'')
                elif button2 in keyboard and button1 not in keyboard:
                    keyboard.row(button2,'')
                
        else:
            button1 = KeyboardButton(datas[0]['carpet'])
            keyboard.row(button1)
        keyboard.add(KeyboardButton("Go Back"))
    else:
        print(f"Request error: {response.status_code}")
    await message.reply("Gilamlar!", reply_markup=keyboard)

@dp.message_handler(Text('Sun\'iy Gazon'))
async def reply_button_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Sun'iy Gazon",request_contact=True, request_location=True, callback_data='disabled'))
    response = requests.get(url=url+'grass/')
    if response.status_code == 200:
        datas = json.loads(response.content)
        if len(datas)>1:
            i = int(len(datas))
            for n in range(0, i,2):
                button1 = KeyboardButton(datas[n - 1]['carpet'])
                button2 = KeyboardButton(datas[n]['carpet'])
                if button1 and button2  not in keyboard  : 
                    keyboard.row(button1, button2)
                elif button1 in keyboard and button2 not in keyboard:
                    keyboard.row(button2,'')
                elif button2 in keyboard and button1 not in keyboard:
                    keyboard.row(button2,'')
        else:
            button1 = KeyboardButton(datas[0]['carpet'])
            keyboard.row(button1)
        keyboard.add(KeyboardButton("Go Back"))
    else:
        print(f"Request error: {response.status_code}")
    await message.reply("Sun'iy Gazon Tanlandi!", reply_markup=keyboard)

@dp.message_handler(Text('Kontakt'))
async def kontakt(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Menejer"))
    keyboard.add(KeyboardButton('Marketing'))
    keyboard.add(KeyboardButton("Go Back"))
    await message.reply("Kontaktlar:",reply_markup=keyboard)

@dp.message_handler(Text('Web Sahifa'))
async def web_site(message: types.Message):
    await bot.send_message(message.chat.id,f"https://www.urgaz.com")

@dp.message_handler(Text('Menejer'))
async def manager(message: types.Message):
    await bot.send_message(message.chat.id,f"Menejer telefon raqami: +998990560000")

@dp.message_handler(Text('Marketing'))
async def marketing(message: types.Message):
    await bot.send_message(message.chat.id,f"Marketing telefon raqami: +998981600066")


@dp.message_handler(lambda message: message.text == 'Go Back')
async def go_back(message: types.Message):
    # "Go Back" tugmasi bosilganda qaytuvchi yuborish
    await send_welcome(message)

    
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_unknown_text(message: types.Message):
    unknown_text = message.text
    response = requests.get(url=url+f"byName/{unknown_text}/")
    if response.status_code==200:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(f"{unknown_text} takibi",request_contact=True, request_location=True, callback_data='disabled'))
        datas = json.loads(response.content)
        if len(datas)>1:
            i = int(len(datas))
            for n in range(0, i,2):
                button1 = KeyboardButton(datas[n-1]['carpet'])
                button2 = KeyboardButton(datas[n]['carpet'])
                keyboard.row(button1, button2)
        else:
            button1 = KeyboardButton(datas[0]['carpet'])
            keyboard.row(button1)
        keyboard.add(KeyboardButton("Go Back"))
        await bot.send_message(message.chat.id, text=unknown_text, reply_markup=keyboard)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Go Back"))
        other_response = requests.get(url=url+f"photo/byName/{unknown_text}/").content
        data = json.loads(other_response)
        await bot.send_photo(message.chat.id,photo=photo_url+data['photo'])



            

# Asosiy funksiya
async def main():
    # Botni boshlaymiz
    await dp.start_polling()

if __name__ == '__main__':
    # main funksiyani ishlatish
    import asyncio
    asyncio.run(main())
