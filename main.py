from flask import Flask, request, render_template
from datetime import datetime
from pathlib import Path

app = Flask(__name__, static_folder="./client", template_folder="./client")  # Настройки приложения

msg_id = 1
all_messages = []
all_users = []


@app.route("/chat")
def chat_page():
    return render_template("chat.html")


def add_user(sender):
    if sender not in all_users:
        all_users.append(sender)


def add_message(sender, text):
    global msg_id
    new_message = {
        "sender": sender,
        "text": text,
        "time": datetime.now().strftime("%H:%M"),
        "msg_id": msg_id
    }
    msg_id += 1
    add_user(sender)
    all_messages.append(new_message)


# API для получения файла со всеми сообщениями
@app.route("/get_messages_to_file")
def get_messages_to_file():
    with open('docs/messages.txt', 'w') as f:
        for msg in all_messages:
            f.write(f"{msg['sender']} : {msg['time']} : {msg['text']}")

    return "Файл располагается в директории сервера (docs/messages.txt)"


# API для получения номера последнего сообщения
@app.route("/get_last_msg_id")
def get_last_msg_id():
    global msg_id
    return {"last_id": msg_id - 1}


# API для удаления сообщений пользвателя
@app.route("/delete_messages")
def delete_messages():
    sender = str(request.args["sender"])

    i = 0
    for msg in all_messages:
        if (msg["sender"] == sender):
            print(f"{msg['text']} : {i}")
            del all_messages[i]
        i += 1

    return "Сообщения удалены"


# API для получения списка пользователей
@app.route("/get_users")
def get_users():

    return {"users": all_users}


# API для получения списка сообщений
@app.route("/get_messages")
def get_messages():
    after = int(request.args["after"])

    messages = []
    for msg in all_messages:
        if (msg["msg_id"] > after):
            messages.append(msg)

    return {"messages": messages}


# HTTP-GET
# API для получения отправки сообщения  /send_message?sender=Mike&text=Hello
@app.route("/send_message")
def send_message():
    sender = request.args["sender"]
    text = request.args["text"]
    add_message(sender, text)
    return {"result": True}


# Главная страница
@app.route("/")
def hello_page():
    return "New text goes here"


app.run()
