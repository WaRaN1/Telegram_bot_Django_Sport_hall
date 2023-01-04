import telebot
from telebot import types
import time
from Sport.models import *


products_all = [el.name for el in Product.objects.all()]
treining_time = ["8:00-9:30", "9:30-11:00", "11:00-12:30", "13:00-14:30", "14:30-16:00", "16:00-17:30", "17:30-19:00"]
treining_day = ["Понеділок", "Вівторок", "Середа", "Четверг", "П'ятниця", "Субота", "Неділя"]

config = {
    "name": "Python_waran_bot",
    "token": "5737862312:AAEjHoaa-Gzxr3JbJx6TzRzBu32Q3NbbppY"
}

free_access = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_registration = types.InlineKeyboardButton("Реєстрація")
button_authorization = types.InlineKeyboardButton("Авторизація")
free_access.add(button_registration, button_authorization)

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_work_with_a_cash = types.InlineKeyboardButton("Робота з рахунком")
button_purchase_of_goods = types.InlineKeyboardButton("Купівля товарів")
button_training = types.InlineKeyboardButton("Тренування")
main_keyboard.add(button_work_with_a_cash, button_purchase_of_goods, button_training)

work_with_a_cash_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_check_account = types.InlineKeyboardButton("Перевірити рахунок")
button_top_up_the_account = types.InlineKeyboardButton("Поповнити рахунок")
button_return_to_the_main_menu = types.InlineKeyboardButton("Повернутись у головне меню")
work_with_a_cash_keyboard.add(button_check_account, button_top_up_the_account, button_return_to_the_main_menu)

trainer_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Вивід всіх наявних тренерів на кнопки
name_trainer = Treiner_warker.objects.all()
name_trainer_all = []
for i in name_trainer:
    trainer_keyboard.add(types.InlineKeyboardButton(f"{i}", f"{i}"))
    name_trainer_all.append(i.name)
button_traine_user = types.InlineKeyboardButton("Повернутись у головне меню")
button_return_to_the_main_menu = types.InlineKeyboardButton("Переглянути замовлені тренування")
trainer_keyboard.add(button_return_to_the_main_menu, button_traine_user)

ivan = telebot.TeleBot(config["token"])

print(name_trainer_all)

@ivan.message_handler(commands=["start"])
def start(message):
    ivan.send_message(message.chat.id,
                      "Вітаємо у системі спортзалу, якщо ви є нашим клієнтом, то пройдіть авторизацію, "
                      "а якщо ні, то ласкаво просимо на реєстрацію", reply_markup=free_access)
    if message.text.lower() == "авторизація":
        ivan.register_next_step_handler(ivan.send_message(message.chat.id, "Введіть пароль для входу"),
                                        authorization)
    elif message.text.lower() == "реєстрація":
        ivan.register_next_step_handler(ivan.send_message(message.chat.id, "Придумайте пароль"), registration)


@ivan.message_handler(content_types=["text"])
def get_text(message):
    print("message: ", message.text)
    var_step = 0
    client = Clients.objects.filter(clients_id=message.chat.id)
    if len(client) > 0:
        client_time = client[0].time_autorization

        if time.time()-client_time < 86400:
            var_step = 1

    if var_step == 1:
        if message.text.lower() in ["робота з рахунком", "перевірити рахунок"]:
            ivan.send_message(message.chat.id, f"Стан вашого рахунку - {client[0].cash_account} ₴",
                              reply_markup=work_with_a_cash_keyboard)

        elif message.text.lower() == "поповнити рахунок":
            ivan.register_next_step_handler(ivan.send_message(message.chat.id, "На яку суму бажаєте поповнити "
                                                                               "рахунок?"), plas_balance)
        elif message.text.lower() == "повернутись у головне меню":
            ivan.send_message(message.chat.id, 'Повернення у головне меню', reply_markup=main_keyboard)

        elif message.text.lower() == "купівля товарів":
            inlines = telebot.types.InlineKeyboardMarkup()
            product = Product.objects.all()
            for elem in product:
                inlines.add(telebot.types.InlineKeyboardButton(text=f"{elem} ₴", callback_data=elem.name))
            inlines.add(
                telebot.types.InlineKeyboardButton(text="------------------------------------------------",
                                                   callback_data="-"))
            inlines.add(telebot.types.InlineKeyboardButton(text="Перевірити рахунок",
                                                           callback_data="Перевірити рахунок"))
            inlines.add(telebot.types.InlineKeyboardButton(text="Переглянути кошик", callback_data="Переглянути кошик"))
            inlines.add(telebot.types.InlineKeyboardButton(text="Провести оплату замовлення",
                                                           callback_data="Провести оплату замовлення"))
            inlines.add(telebot.types.InlineKeyboardButton(text="Очистити кошик", callback_data="Очистити кошик"))
            ivan.send_message(message.chat.id, "Сьогоднішній перелік товарів:", reply_markup=inlines)

        elif message.text.lower() == "тренування":
            print("1")
            ivan.register_next_step_handler(
                ivan.send_message(message.chat.id, "Оберіть одного з наших тренерів", reply_markup=trainer_keyboard),
                trainer_time)

        elif message.text in name_trainer_all:
            ivan.send_message(message.chat.id, trainer_time)

    else:
        if message.text.lower() == "авторизація":
            ivan.register_next_step_handler(ivan.send_message(message.chat.id, "Введіть пароль для входу"),
                                            authorization)
        elif message.text.lower() == "реєстрація":
            ivan.register_next_step_handler(ivan.send_message(message.chat.id, "Придумайте пароль"), registration)

        else:
            ivan.send_message(message.chat.id, "Для доступу до функціоналу бота пройдіть авторизацію",
                              reply_markup=free_access)


#

#

#

#
#         elif message.text.lower() == "переглянути замовлені тренування":  # Вивід всіх передзамовлених тренувань з тренером
#             ivan.send_message(message.chat.id, rozcklad_all(message))
#     else:

#         else:
#             ivan.send_message(message.chat.id, "Для доступу до функціоналу бота пройдіть авторизацію",
#                               reply_markup=free_access)

# def rozcklad_all(message):
#     with open(trainer_all_time, "r", encoding='utf-8') as r_file:
#         trainer_time_all = json.load(r_file)
#     rozcklad = "Призначені тренування на наступний тиждень:\n\n"
#     for el in trainer_time_all:
#         for elem in trainer_time_all[el]:
#             for tim in trainer_time_all[el][elem]:
#                 if trainer_time_all[el][elem][tim] == str(message.chat.id):
#                     name_trainer_a = trainer_time_all[el][elem]
#                     for i in trainer_time_all[el].keys():
#                         if trainer_time_all[el][i] == name_trainer_a:
#                             rozcklad += f"День тренування: {el}\n"
#                             rozcklad += f"Час тренування:    {elem}\n"
#                             for i in trainer_time_all[el][elem].keys():
#                                 if trainer_time_all[el][elem][i] == str(message.chat.id):
#                                     rozcklad += f"Ваш тренер:            {i}\n\n"
#                             break
#     return rozcklad
#

#
#
# def check_account(message):  # Функція для перевірки баланса
#     file = open(clients, "r", encoding='utf-8')
#     all_users = file.read().split("\n")
#     file.close()
#     user_balance = ""
#     for el in all_users:
#         if el.split("/")[0] == str(message.chat.id):
#             user_balance = float(el.split("/")[3])
#     return user_balance
#
#
# def product():
#     file = open(product_shop, "r", encoding='utf-8')
#     product = file.read().split("\n")
#     file.close()
#     return product
#
#
# def chec_user_prod(call):
#     with open(user_product, "r", encoding='utf-8') as r_file:
#         user_prod = json.load(r_file)
#     user_prod_var = ""
#     user_prod_sum = 0.0
#     for i in user_prod[f"{call.message.chat.id}"]:
#         user_prod_var += f"{i}\n"
#         user_prod_sum += user_prod[f'{call.message.chat.id}'][i]
#     all_info_user_prod = [user_prod_var, user_prod_sum]
#     return all_info_user_prod


@ivan.callback_query_handler(func=lambda call: True)
def callback_data(call):
    print("call.data: ", call.data)
    if call.data in products_all:   # Ще не працює, проблема з forenkey
        product = Product.objects.filter(name=call.data)
        try:
            _, created = User_product.objects.get_or_create(
                clients=call.message.chat.id,
                name=product[0].name,
                price=product[0].price,
            )
            print("1")
            print(call.message.chat.id)
            print(product[0].name)
            print(product[0].price)
        except:
            print("2")
            print(call.message.chat.id)
            print(product[0].name)
            print(product[0].price)
            pass

    elif call.data == "Перевірити рахунок":
        client = Clients.objects.filter(clients_id=call.message.chat.id)
        ivan.send_message(call.message.chat.id, f"Стан вашого рахунку - {client[0].cash_account} ₴",
                          reply_markup=main_keyboard)

    elif call.data == "Переглянути кошик":
        inlines = telebot.types.InlineKeyboardMarkup()
        products = User_product.objects.all()
        sum = 0.0
        for elem in products:
            sum += int(elem.price)
            inlines.add(telebot.types.InlineKeyboardButton(text=f"{elem.name} ₴", callback_data=f"{elem.name}"))
        inlines.add(
            telebot.types.InlineKeyboardButton(text="------------------------------------------------",
                                               callback_data="-"))
        inlines.add(telebot.types.InlineKeyboardButton(text="Провести оплату замовлення",
                                                       callback_data="Провести оплату замовлення"))
        inlines.add(telebot.types.InlineKeyboardButton(text="Очистити кошик", callback_data="Очистити кошик"))

        ivan.send_message(call.message.chat.id, f"Загальна сумма: {sum}₴", reply_markup=inlines)

    elif call.data == "Очистити кошик":
        User_product.objects.all().delete()

    elif call.data == "Провести оплату замовлення":
        sum_1 = Clients.objects.filter(clients_id=call.message.chat.id)
        products = User_product.objects.all()
        sum_all = 0
        for elem in products:
            sum_all += int(elem.price)
        cash = Clients.objects.filter(clients_id=call.message.chat.id).update(cash_account=sum_1[0].cash_account - sum_all)
        client = Clients.objects.filter(clients_id=call.message.chat.id)
        # User_product.objects.all().delete()
        ivan.send_message(call.message.chat.id, f"Оплату проведено. Стан вашого рахунку - {client[0].cash_account} ₴",
                          reply_markup=main_keyboard)

    elif call.data.split(",")[0] in treining_day and call.data.split(",")[1] in treining_time\
            and call.data.split(",")[2] in name_trainer_all:
        print("yes")
        try:
            _, created = Schedule_treiner.objects.get_or_create(
                weekday=call.data.split(",")[0],
                treiner_name=call.data.split(",")[1],
                time_training=call.data.split(",")[2],
                clients=call.message.chat.id
            )
            print("11")
        except:
            print("22")
            pass

def registration(message):
    password = message.text
    try:
        _, created = Clients.objects.get_or_create(

            clients_id=message.chat.id,
            password=password,
            time_autorization=0.0,
            cash_account=0,
        )
    except:
        print("No")
        pass
    ivan.send_message(message.chat.id, f"Вітаю, вас успішно зареєстровано у системі, отримайте вашу карту та "
                                       f"авторизуйтесь для входу")


def authorization(message):
    client = Clients.objects.filter(clients_id=message.chat.id)
    if len(client) > 0:
        if client[0].password == message.text:
            Clients.objects.filter(clients_id=message.chat.id).update(time_autorization=time.time())
            ivan.send_message(message.chat.id, f"Вітаємо вас у системі",
                                                          reply_markup=main_keyboard)
        else:
            ivan.send_message(message.chat.id, f"Невірно введений пароль")
    else:
        ivan.send_message(message.chat.id, f"Ви не зареєстровані у системиі")


def plas_balance(message):
    client = Clients.objects.filter(clients_id=message.chat.id)
    Clients.objects.filter(clients_id=message.chat.id).update(cash_account=client[0].cash_account +
                                                                           int(float(message.text))) # Без float б'є помилку при введенні у телеграм числа через крапку
    plas_balance = "https://www.portmone.com.ua/popovnyty-rakhunok-mobilnoho?gclid=Cj0KCQiA45qdBhD-ARIsAOHbVdFrlNp38FMOhwif78In6fNRi-hlSVrfjlOp6US5LeP3dsr37Z9OzjQaAvNyEALw_wcB"
    ivan.send_message(message.chat.id, plas_balance)


def trainer_time(message):
    if message.text.lower() == "повернутись у головне меню":  # Щоб уникнути крашу при виборі не тренера а повернення у головне меню
        ivan.send_message(message.chat.id, 'Повернення у головне меню', reply_markup=main_keyboard)
    # elif message.text.lower() == "переглянути замовлені тренування":    # Щоб уникнути крашу при виборі не тренера а перерегляд замовлених тренувань
    #     ivan.send_message(message.chat.id, rozcklad_all(message))
    else:
        treiner = Treiner_warker.objects.filter(name=message.text)
        for el in treiner:
            treiner_id = el.id
        treiner_data = Schedule_treiner.objects.filter(treiner_name=treiner_id)
        dict_schedule_treiner = {}
        for elem in treiner_data:
            dict_schedule_treiner[elem.weekday] = elem.time_training
        inlines = telebot.types.InlineKeyboardMarkup()
        for elem_day in treining_day:
            inlines.add(telebot.types.InlineKeyboardButton(text=f"-----------------    {elem_day}    -----------------",
                                                           callback_data=f"{1}"))
            for elem_time in treining_time:
                if elem_day in dict_schedule_treiner:
                    if elem_time == dict_schedule_treiner[elem_day]:
                        continue
                    else:
                        inlines.add(telebot.types.InlineKeyboardButton(text=f"{elem_time}",
                                                                       callback_data=f"{elem_day},{elem_time},"
                                                                                     f"{message.text}"))
                else:
                    inlines.add(telebot.types.InlineKeyboardButton(text=f"{elem_time}",
                                                                   callback_data=f"{elem_day},{elem_time},"
                                                                                     f"{message.text}"))
        ivan.send_message(message.chat.id, f'Ви обрали тренера {message.text}. Оберіть день для тренувань та час',
                        reply_markup=inlines)


ivan.polling(none_stop=True, interval=0)