import requests
import datetime
import psutil
import config
import persistence
import time
# from persistence import Persistence

last_notification = 0
# storage = Persistence()


def processMessage(message, in_reply_to):
    if message.startswith("/"): processCommandMessage(message, in_reply_to)


def processCommandMessage(message, in_reply_to):
    command = message
    if "@" in command:
        command, botname = command.split("@", 1)
        if botname.lower() != config.NAME.lower():
            # Ignore messages for other bots
            return

    # if command == "/start":
    #     commandStart(message, in_reply_to)
    # elif command == "/stop":
    #     commandStop(message, in_reply_to)
    if command == "/help":
        commandHelp(in_reply_to)
    elif command == "/usage":
        commandUsage(in_reply_to)
    elif command == "/users":
        commandUsers(in_reply_to)
    elif command == "/disks":
        commandDisks(in_reply_to)
    else:
        sendTextMessage("Sorry, no such command.", in_reply_to)


'''
Send a text message to particular chat with given chat_id 
'''
def sendTextMessage(text, in_reply_to = None):

    post_url = config.POSTS_API_URL
    payload = {
    "channel_id": config.CHANNEL_ID,
    "message": text,
    "root_id": in_reply_to,
    "file_ids": [],
    "props": ""
    }
    response = requests.request("POST", url, data=payload, headers=config.HEADERS)

def sendAuthMessage():
    sendTextMessage("Please sign in!")

# def startupMessage():
#     for id in storage.allUsers():
#         sendTextMessage(id, "Bot Started up")

# def shutdownMessage():
#     for id in storage.allUsers():
#         sendTextMessage(id, "Bot dead")


'''
COMMANDS SECTION BEGIN

Below are the list of commands to be executed
'''

# def commandStart(message, irt):
#     sendTextMessage("Booting up bot")
#     else:
#         if parameter.strip() == config.PASSWORD:
#             storage.registerUser(chat_id)
#             sendTextMessage(chat_id, "Thank you. Type /help for options")
#         else:
#             sendTextMessage(chat_id, "Error logging in. Type /start <password> to start")

# def commandStop(message):
#     chat_id = message["chat"]["id"]
#     if storage.isRegisteredUser(chat_id):
#         storage.unregisterUser(chat_id)
#         sendTextMessage(chat_id, "Killing bot.")
#     else:
#         sendAuthMessage(chat_id)

def commandHelp(irt):
    # chat_id = message["chat"]["id"]
    sendTextMessage(config.NAME + """
        Monitor status of server.
        /usage - View active usage
        /users - View users
        /disks - View disk usage""", 
        irt
    )

def commandUsage(irt):
    # chat_id = message["chat"]["id"]
    # if not storage.isRegisteredUser(chat_id):
        # sendAuthMessage(chat_id)
        # return

    text = """Uptime: {0}
        CPU: {1} %
        RAM: {2} %
        Swap: {3} %""".format(
            str(datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())),
            psutil.cpu_percent(),
            psutil.virtual_memory().percent,
            psutil.swap_memory().percent
        )

    sendTextMessage(text, irt)

def commandUsers(irt):
    # chat_id = message["chat"]["id"]
    # if not storage.isRegisteredUser(chat_id):
        # sendAuthMessage(chat_id)
        # return

    text = ""
    for user in psutil.users():
        text = text + "{0}@{1} {2}\n".format(user.name, user.host, str(datetime.datetime.fromtimestamp(user.started)))

    sendTextMessage(text, irt)

def commandDisks(message):
    # chat_id = message["chat"]["id"]
    # if not storage.isRegisteredUser(chat_id):
    #     sendAuthMessage(chat_id)
    #     return

    text = ""
    for dev in psutil.disk_partitions():
        text = text + "{0} ({1}) {2} %\n".format(dev.device, dev.mountpoint, psutil.disk_usage(dev.mountpoint).percent)

    sendTextMessage(text, irt)

'''
COMMANDS SECTION END
'''

def alarms():
    global last_notification
    now = time.time()

    delta_t = now - last_notification
    if config.ENABLE_NOTIFICATIONS and (delta_t > config.NOTIFCATION_INTERVAL):
        text = "Alarm!\n"
        should_send = False

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        if cpu > config.NOTIFY_CPU_PERCENT:
            text = text + "CPU: {0} %\n".format(cpu)
            should_send = True
        if ram > config.NOTIFY_RAM_PERCENT:
            text = text + "RAM: {0} %\n".format(ram)
            should_send = True

        if should_send:
            last_notification = now
            sendTextMessage(text)
