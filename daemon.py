import requests
import config
import methods
import atexit

last_update_id = None

# methods.startupMessage()
# atexit.register(methods.shutdownMessage)

while True:
    methods.alarms()
    try: 
        post_url = config.UPDATES_API_URL
        querystring ={"after":last_update_id}
        r = requests.request("GET", post_url, headers=config.HEADERS, params = querystring)
        result = r.json()

        if result["order"] != []:

            post_ids = result["order"]
            last_post_id = post_ids[0]

            if last_post_id != last_update_id: 
                last_update_id = last_post_id
                # print(result["posts"][last_update_id]['message'])
                methods.processMessage(result["posts"][last_update_id]['message'], last_update_id)

    except KeyboardInterrupt:
        print("Terminating Server")
        break