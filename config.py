# Mattermost details
NAME = "eyuptime_bot"
CHANNEL_ID = "qkmgmk13738txq8kwfdd5bj58e"
USER_ID = ""
POSTS_API_URL = "https://chat.eydean.com/api/v4/posts"
UPDATES_API_URL =  "https://chat.eydean.com/api/v4/channels/"+CHANNEL_ID+"/posts" 
HEADERS = {
            'Authorization': "Bearer jkpgwypn47bstq6ye18hkmp9zw",
            'Content-Type': "application/json"
            }

TIMEOUT = 60 * 5
ENABLE_NOTIFICATIONS = True
NOTIFCATION_INTERVAL = 60
NOTIFY_CPU_PERCENT = 50
NOTIFY_RAM_PERCENT = 50
