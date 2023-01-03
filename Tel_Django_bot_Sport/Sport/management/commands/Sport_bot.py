import telebot
from telebot import types
import time
from Sport.models import *


products_all = [el.name for el in Product.objects.all()]


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
for i in name_trainer:
    trainer_keyboard.add(types.InlineKeyboardButton(f"{i}", f"{i}"))
button_traine_user = types.InlineKeyboardButton("Повернутись у головне меню")
button_return_to_the_main_menu = types.InlineKeyboardButton("Переглянути замовлені тренування")
trainer_keyboard.add(button_return_to_the_main_menu, button_traine_user)

ivan = telebot.TeleBot(config["token"])


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
#         elif message.text.lower() == "тренування":
#             ivan.register_next_step_handler(
#                 ivan.send_message(message.chat.id, "Оберіть одного з наших тренерів", reply_markup=trainer_keyboard),
#                 trainer_time)
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
# def trainer_time(message):
#     if message.text.lower() == "повернутись у головне меню":  # Щоб уникнути крашу при виборі не тренера а повернення у головне меню
#         ivan.send_message(message.chat.id, 'Повернення у головне меню', reply_markup=main_keyboard)
#     elif message.text.lower() == "переглянути замовлені тренування":    # Щоб уникнути крашу при виборі не тренера а перерегляд замовлених тренувань
#         ivan.send_message(message.chat.id, rozcklad_all(message))
#     else:
#         ivan.send_message(message.chat.id, f'Ви обрали тренера {message.text}. Оберіть день для тренувань та час')
#         with open(trainer_all_time, "r", encoding='utf-8') as r_file:
#             trainer_time_all = json.load(r_file)
#         inlines_time = telebot.types.InlineKeyboardMarkup()
#         for day in trainer_time_all:
#             inlines_time.add(
#                 telebot.types.InlineKeyboardButton(text=f"-----------------       {day}       -----------------",
#                                                    callback_data=day))
#             for time_d in trainer_time_all[day]:
#                 if message.text not in trainer_time_all[day][time_d]:
#                     inlines_time.add(telebot.types.InlineKeyboardButton(text=time_d, callback_data=f"{day}/{time_d}"))
#         ivan.send_message(message.chat.id, f"{message.text}", reply_markup=inlines_time)
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
    if call.data in products_all:
        product = Product.objects.filter(name=call.data)
        try:
            _, created = User_product.objects.get_or_create(
                clients=call.message.chat.id,
                name=product[0].name,
                price=product[0].price,
            )
        except:
            pass

    elif call.data == "Перевірити рахунок":
        client = Clients.objects.filter(clients_id=call.message.chat.id)
        ivan.send_message(call.message.chat.id, f"Стан вашого рахунку - {client[0].cash_account} ₴",
                          reply_markup=main_keyboard)

    elif call.data == "Переглянути кошик":
        inlines = telebot.types.InlineKeyboardMarkup()
        products = User_product.objects.all()
        for elem in products:
            print(elem.name)
            inlines.add(telebot.types.InlineKeyboardButton(text=f"{elem} ₴", callback_data=elem.name))
        # inlines.add(
        #     telebot.types.InlineKeyboardButton(text="------------------------------------------------",
        #                                        callback_data="-"))
        # inlines.add(telebot.types.InlineKeyboardButton(text="Провести оплату замовлення",
        #                                                callback_data="Провести оплату замовлення"))
        # inlines.add(telebot.types.InlineKeyboardButton(text="Очистити кошик", callback_data="Очистити кошик"))
        ivan.send_message(call.message.chat.id, "Сьогоднішній перелік товарів:", reply_markup=inlines)


    # product = Product.objects.all()
    # for elem in product:
    #     if call.data == elem.name:


    # if call.data in product():  # Перевірка чи є натиснена кнопка переліком товару
    #     ivan.send_message(call.message.chat.id, f"{call.data} ₴ додано до кошика")
    #     with open(user_product, "r", encoding='utf-8') as r_file:
    #         user_prod = json.load(r_file)
    #     if call.data.split(' - ')[0] in user_prod[
    #         f"{call.message.chat.id}"].keys():  # Перевіряємо чи є у корзині такий товару
    #         user_prod[f"{call.message.chat.id}"][call.data.split(' - ')[0]] += float(call.data.split(' - ')[1])
    #     else:
    #         user_prod[f"{call.message.chat.id}"][call.data.split(' - ')[0]] = float(call.data.split(' - ')[1])
    #     with open(user_product, "w", encoding='utf-8') as w_file:
    #         json.dump(user_prod, w_file, ensure_ascii=False)
    #
    # elif call.data.lower() == "переглянути кошик":
    #     ivan.send_message(call.message.chat.id,
    #                       f"Ви замовили товари:\n{chec_user_prod(call)[0]}\n Сума покупки: {chec_user_prod(call)[1]} ₴")
    #
    # elif call.data.lower() == "перевірити рахунок":
    #     ivan.send_message(call.message.chat.id, f"Стан вашого рахунку - {check_account(call.message)} ₴")
    #
    # elif call.data.lower() == "очистити кошик":
    #     clear_user_product(call)
    #     ivan.send_message(call.message.chat.id, "Кошик очищено")
    #
    # elif call.data.lower() == "провести оплату замовлення":
    #     ivan.send_message(call.message.chat.id, "Оплату проведено", minus_balance(call))
    #     clear_user_product(call)
    #
    # elif call.message.text in name_trainer:
    #     with open(trainer_all_time, "r", encoding='utf-8') as r_file:
    #         n_d_t = json.load(r_file)
    #     print(n_d_t[call.data.split("/")[0]][call.data.split("/")[1]])
    #     n_d_t[call.data.split("/")[0]][call.data.split("/")[1]].update(
    #         {f"{call.message.text}": f"{call.message.chat.id}"})
    #     with open(trainer_all_time, "w", encoding='utf-8') as w_file:
    #         json.dump(n_d_t, w_file, ensure_ascii=False)


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

#
# def minus_balance(call):
#     file = open(clients, "r", encoding='utf-8')
#     all_users = file.read().split("\n")
#     file.close()
#     rez_sum = ""
#     for ind in range(len(all_users)):
#         if all_users[ind].split("/")[0] == str(call.message.chat.id):
#             rez_sum = float(all_users[ind].split('/')[3]) - chec_user_prod(call)[1]
#             all_users[ind] = f"{all_users[ind].split('/')[0]}/{all_users[ind].split('/')[1]}/{all_users[ind].split('/')[2]}/{rez_sum}"
#             break
#     var_var = ''
#     for ind in range(len(all_users)):
#         var_var += f'{all_users[ind]}\n'
#     file = open(clients, "w", encoding='utf-8')
#     file.write(var_var[0:len(var_var) - 1])
#     file.close()
#     ivan.send_message(call.message.chat.id, f"Залишок на рахунку {rez_sum} ₴")
#
#
# def clear_user_product(call):
#     with open(user_product, "r", encoding='utf-8') as r_file:
#         user_prod = json.load(r_file)
#     user_prod[f'{call.message.chat.id}'] = {}
#     with open(user_product, "w", encoding='utf-8') as w_file:
#         json.dump(user_prod, w_file, ensure_ascii=False)


ivan.polling(none_stop=True, interval=0)