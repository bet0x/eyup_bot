import requests
import config
import methods
import atexit

last_update_id = 0

# methods.startupMessage()
# atexit.register(methods.shutdownMessage)

while True:
    # methods.alarms()
    try: 
        #print("Make request: {0}".format(last_update_id))
        post_url = config.UPDATES_API_URL
        querystring ={"after":last_update_id}
        headers = {
            'Authorization': "Bearer jkpgwypn47bstq6ye18hkmp9zw",
            'Content-Type': "application/json"
            }
        r = requests.request("GET", post_url, headers=headers)#, params = querystring)
        print(r)
        result = r.json()
        print(result)
        if "ok" not in result:
            break
        '''
                for update in result["result"]:
                    update_id = update["update_id"]
                    if update_id > last_update_id:
                        last_update_id = update_id

                    methods.processMessage(update["message"])
            else:
                print(result)
        '''
    except KeyboardInterrupt:
        print("Terminating Server")
        break