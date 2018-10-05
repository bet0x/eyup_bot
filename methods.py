import requests
import datetime
import psutil
import config
import time

last_notification = 0

'''
Process message only if it starts with a hyphen(-).
'''
def processMessage(message, in_reply_to):
    if message.startswith("-"): processCommandMessage(message, in_reply_to)


''' 
Split message into command and bot name, process further if bot name mentioned
'''
def processCommandMessage(message, in_reply_to):
    if "@" in message:
        command, botname = message.split("@", 1)
        # Ignore messages for other bots
        if botname.lower() != config.NAME.lower():
            return
    else:
        command = None

    if command == "-help":
        commandHelp(in_reply_to)
    elif command == "-usage":
        commandUsage(in_reply_to)
    elif command == "-users":
        commandUsers(in_reply_to)
    elif command == "-disks":
        commandDisks(in_reply_to)
    else:
        sendTextMessage("Sorry, no such command.", in_reply_to)


'''
Write a post in reply to command 
'''
def sendTextMessage(text, in_reply_to = ""):

    post_url = config.POSTS_API_URL
    payload = {
    "channel_id": config.CHANNEL_ID,
    "message": text,
    "root_id": in_reply_to
    }
    response = requests.request("POST", post_url, json=payload, headers=config.HEADERS)
    if response.status_code != 201:
        print("Error encountered whilst writing post.")

'''
COMMANDS SECTION BEGIN

Below are the list of commands to be executed
'''
def commandHelp(irt):
    sendTextMessage(config.NAME + """
        Monitor status of server.
        -usage - View active usage
        -users - View users
        -disks - View disk usage""", 
        irt
    )

def commandUsage(irt):
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
    text = ""
    for user in psutil.users():
        text = text + "{0}@{1} {2}\n".format(user.name, user.host, str(datetime.datetime.fromtimestamp(user.started)))

    sendTextMessage(text, irt)

def commandDisks(irt):

    text = ""
    for dev in psutil.disk_partitions():
        text = text + "{0} ({1}) {2} %\n".format(dev.device, dev.mountpoint, psutil.disk_usage(dev.mountpoint).percent)

    sendTextMessage(text, irt)


'''
Alarm goes off in 2 cases
    If CPU usage > threshold 
    If RAM usage > threshold
'''
def alarms():
    global last_notification
    
    # Get current time
    now = time.time()

    # Calculate last post time
    delta_t = now - last_notification

    # if last post time > threshold and notifications enabled, send alert
    if config.ENABLE_NOTIFICATIONS and (delta_t > config.NOTIFCATION_INTERVAL):
        text = "ALERT!\n"
        should_send = False

        # Get CPU and RAM usage
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        # CPU usage compare
        if cpu > config.NOTIFY_CPU_PERCENT:
            text = text + "CPU: {0} %\n".format(cpu)
            should_send = True
        # RAM usage compare
        if ram > config.NOTIFY_RAM_PERCENT:
            text = text + "RAM: {0} %\n".format(ram)
            should_send = True

        if should_send:
            last_notification = now
            sendTextMessage(text)
