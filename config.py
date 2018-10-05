# Mattermost details
NAME = "eyup_bot"
CHANNEL_ID = ""
USER_ID = ""
POSTS_API_URL = "https://chat.eydean.com/api/v4/posts"
UPDATES_API_URL =  "https://chat.eydean.com/api/v4/channels/"+CHANNEL_ID+"/posts" 
HEADERS = {
            'Authorization': "Bearer ",
            'Content-Type': "application/json"
            }

TIMEOUT = 1
ENABLE_NOTIFICATIONS = True
NOTIFCATION_INTERVAL = 60
NOTIFY_CPU_PERCENT = 50
NOTIFY_RAM_PERCENT = 50
