import telebot
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from telebot import types # для указание типов
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Импортируем библиотеки
token = "6829684003:AAE3dkwihgidrZfOCPouDIEJhwqXpRlU-W0" #подключаем бота
bot=telebot.TeleBot(token, parse_mode=None)
i = 0 #Переменная для повторения циклов (on/off)
usernameStr = '' #Данные аккаунта для входа
passwordStr = ''
url = "https://178fz.roseltorg.ru/#auth/login" #Ссылка на вход
browser = webdriver.Chrome() #Открывает браузер
browser.get(url)

#команда старт
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #выдаём клавиатуру
    btn1 = types.KeyboardButton("/on")
    btn2 = types.KeyboardButton("/off")
    markup.add(btn1, btn2)
    bot.reply_to(message, "Список команд: \n/on - делает парсер активным \n/off - делает парсер неактивным и сбрасывает ссылку \n/parser [ваша ссылка] - позволяет задать ссылку первому парсеру и выводит данные \n/parser2 [ваша ссылка] - тоже, что и просто /parser одновременно с ним, но по другой ссылке ", reply_markup=markup)
    

#Команда включения
@bot.message_handler(commands=['on'])
def baba_s_bebe(message):
    global i
    global a
    i = 1 #Меняем i с 0 на 1 для включения
    a = 1 #Тоже самое только для второго парсера
    time.sleep(5)
    print(i)
    bot.reply_to(message, "Парсер активен")

@bot.message_handler(commands=['off'])
def baba_s_bebe(message):
    global i
    global a
    i = 0
    a = 0
    print(i)
    bot.reply_to(message, "Парсер не активен и сброшен ", reply_markup=types.ReplyKeyboardRemove())
    print (a,i)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/on")
    btn2 = types.KeyboardButton("/off")
    btn3 = types.KeyboardButton("/start")
    markup.add(btn1, btn2, btn3)
    bot.reply_to(message, "Желаете его включить?", reply_markup=markup)

@bot.message_handler(commands=['parser'])
def baba_s_bebe(message):
    log = WebDriverWait(browser, 500).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div/form/div[1]/div[1]/input')))
    log.clear() #очищаем строчки для входа
    log.send_keys(usernameStr) #отправляем логин
    password = WebDriverWait(browser, 500).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ext-gen48"]')))
    password.clear() #отправляем пароль
    password.send_keys(passwordStr)
    time.sleep(3)
    browser.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/table/tbody/tr[2]/td[2]/em/button").click()
    message.text = message.text.replace("/parser","") #удаляем текст команды для получения ссылки
    url = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn3 = types.KeyboardButton("/off")
    markup.add(btn3)
    bot.reply_to(message, f'Ваша ссылка на первом потоке: {message.text}', reply_markup=markup)
  
    url = message.text
    browser.execute_script(f'window.open("{url}")') #открываем ссылку в новом окне, чтобы аккаунт не вылетел
    browser.get(url)
    while i == 1:
            time.sleep(10)
            #Получаем с сайта элементы
            share =  browser.find_element(By.XPATH,  '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div/form/div[1]/div/div/table/tbody/tr[1]/td[1]/div/div/div/div[10]/div/div')
            share2 = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div/form/div[1]/div/div/table/tbody/tr[1]/td[1]/div/div/div/div[2]/div/div")
            share3 = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div/form/div[1]/div/div/table/tbody/tr[1]/td[1]/div/div/div/div[9]/div/div/b")
            print(share.text)
            print(share3.text) #парсим
            if share.text != 'Времени до завершения торгов: --:--':
                if share3 != "1" or "2": #ТЕСТОВАЯ ЧАСТЬ МОЖЕТ НЕ РАБОТАТЬ (только это строчка всё остальное должно)
                     bot.reply_to(message, f"{share.text}\nВаша позиция: {share3.text}\n{share2.text}")
                else:
                     print("Ждём 1")
            else:
                btn1 = types.KeyboardButton("/on")
                btn3 = types.KeyboardButton("/start")
                markup.add(btn1, btn3)
                bot.reply_to(message, f"Время аукциона истекло",reply_markup=markup)
                break

@bot.message_handler(commands=['parser2'])
def baba_s_bebe2(message):
    log = WebDriverWait(browser, 500).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div/form/div[1]/div[1]/input')))
    log.clear()
    log.send_keys(usernameStr)
    password = WebDriverWait(browser, 500).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ext-gen48"]')))
    password.clear()
    password.send_keys(passwordStr)
    time.sleep(3)
    browser.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/table/tbody/tr[2]/td[2]/em/button").click()
    message.text = message.text.replace("/parser","")
    url = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn3 = types.KeyboardButton("/off")
    markup.add(btn3)
    bot.reply_to(message, f'Ваша ссылка на первом потоке: {message.text}', reply_markup=markup)
  
    url = message.text
    browser.execute_script(f'window.open("{url}")')
    browser.get(url)
    while i == 1:
            time.sleep(10)
            share4 =  browser.find_element(By.XPATH,  '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div/form/div[1]/div/div/table/tbody/tr[1]/td[1]/div/div/div/div[10]/div/div')
            share5 = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div/form/div[1]/div/div/table/tbody/tr[1]/td[1]/div/div/div/div[2]/div/div")
            share6 = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div/form/div[1]/div/div/table/tbody/tr[1]/td[1]/div/div/div/div[9]/div/div")
            print(share4.text)
            print(share6.text)
            if share4.text != 'Времени до завершения торгов: --:--':
                if share6 != "1" or "2":
                     bot.reply_to(message, f"{share4.text}\nВаша позиция: {share6.text}\n{share5.text}")
                else:
                     print("Ждём") 
            else:
                btn1 = types.KeyboardButton("/on")
                btn3 = types.KeyboardButton("/start")
                markup.add(btn1, btn3)
                bot.reply_to(message, f"Время аукциона истекло",reply_markup=markup)
                break
bot.infinity_polling() #Запуск бота