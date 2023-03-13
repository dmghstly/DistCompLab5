import asyncio
from pyodide.http import pyfetch
import json

last_seen_id = 0
first_id = 0
start = True
# Находим элементы интерфейса по их ID
send_message = document.getElementById("send_message")
delete_all = document.getElementById("delete_all")
delete_yours = document.getElementById("delete_yours")
sender = document.getElementById("sender")
message_text = document.getElementById("message_text")
user_window = document.getElementById("user_window")
chat_window = document.getElementById("chat_window")

async def fetch(url, method, payload=None):
    kwargs = {
        "method": method
    }
    if method == "POST":
        kwargs["body"] = json.dumps(payload)
        kwargs["headers"] = {"Content-Type": "application/json"}
    return await pyfetch(url, **kwargs)

def set_timeout(delay, callback):
    def sync():
        asyncio.get_running_loop().run_until_complete(callback())

    asyncio.get_running_loop().call_later(delay, sync)

# Добавляет список пользователей
def append_message(message):
    # Создаем HTML-элемент представляющий сообщение
    item = document.createElement("li")  # li - это HTML-тег для элемента списка
    item.className = "list-group-item"   # className - определяет как элемент выглядит
    # Добавляем его в список сообщений (chat_window)
    item.innerHTML = f'[<b>{message["sender"]}</b>]: <span>{message["text"]}</span><span class="badge text-bg-light text-secondary">{message["time"]}</span>'
    chat_window.prepend(item)

# Добавляет пользователя на форму
def append_user(user):
    # Создаем HTML-элемент представляющий сообщение
    item = document.createElement("li")  # li - это HTML-тег для элемента списка
    item.className = "list-group-item"   # className - определяет как элемент выглядит
    # Добавляем его в список сообщений (user_window)
    item.innerHTML = f'<span>{user}</span>'
    user_window.prepend(item)

# Добавляет новое сообщение в список сообщений
def append_message(message):
    # Создаем HTML-элемент представляющий сообщение
    item = document.createElement("li")  # li - это HTML-тег для элемента списка
    item.className = "list-group-item"   # className - определяет как элемент выглядит
    # Добавляем его в список сообщений (chat_window)
    item.innerHTML = f'[<b>{message["sender"]}</b>]: <span>{message["text"]}</span><span class="badge text-bg-light text-secondary">{message["time"]}</span>'
    chat_window.prepend(item)

# Вызывается при клике на send_message
async def send_message_click(e):
    # Отправляем запрос
    await fetch(f"/send_message?sender={sender.value}&text={message_text.value}", method="GET")
    # Очищаем поле
    message_text.value = ""

# Вызывается при клике на delete_all
async def dalete_all_click(e):
    global last_seen_id
    global first_id
    # Обновляем данные
    first_id = last_seen_id + 1
    # Очищаем поле для сообщений
    chat_window.innerHTML = ""

# Вызывается при клике на delete_all
async def dalete_yours_click(e):
    if (sender.value != None):
        result = await fetch(f"/delete_messages?sender={sender.value}", method="GET")
        result = await fetch(f"/delete_messages?sender={sender.value}", method="GET")
        result = await fetch(f"/delete_messages?sender={sender.value}", method="GET")
        result = await fetch(f"/delete_messages?sender={sender.value}", method="GET")

# Загружает всех пользователей на форму
async def load_users():
    result = await fetch(f"/get_users", method="GET")  # Делаем запрос
    user_window.innerHTML = ""  # Очищаем окно с пользователями
    data = await result.json()
    all_users = data["users"]  # Берем список сообщений из ответа сервера
    for user in all_users:
        append_user(str(user))
    set_timeout(2, load_users) # Запускаем загрузку заново через секунду


# Загружает новые сообщения с сервера и отображает их
async def load_fresh_messages():
    global last_seen_id
    global start
    global first_id
    # Загружать только новые сообщения
    result = await fetch(f"/get_messages?after={first_id}", method="GET")  # Делаем запрос
    chat_window.innerHTML = ""  # Очищаем окно с сообщениями
    data = await result.json()
    all_messages = data["messages"]  # Берем список сообщений из ответа сервера
    if (start):
        if (len(all_messages) == 0):
            first_id = 0
            last_seen_id = 0
        else:
            msg = all_messages[-1]
            first_id = msg["msg_id"]
            last_seen_id = msg["msg_id"]
        start = False
    else:
        i = 1
        for msg in all_messages:
            if (i == len(all_messages)):
                last_seen_id = msg["msg_id"]  # msg_id Последнего сообщение
            append_message(msg)
            i += 1
    set_timeout(2, load_fresh_messages) # Запускаем загрузку заново через секунду


# Устнаваливаем действие при клике
send_message.onclick = send_message_click
delete_all.onclick = dalete_all_click
delete_yours.onclick = dalete_yours_click
#append_message({"sender":"Елена Борисовна", "text":"Присылаем в чат только рабочие сообщения!!!", "time": "00:01"})
asyncio.ensure_future(load_users())
asyncio.ensure_future(load_fresh_messages())
