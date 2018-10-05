import requests
import config
import methods
# import atexit
import time

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

        '''
        Sample response
        {
            "order": ["post_id1","post_id12"],
            "posts": {
                "post_id12": {... content ... },
                "post_id1": {... content ... }
            }
        }
        '''

        # If result obtained and pending posts exist
        if r.status_code == 200 and result["order"] != []:

            post_ids = result["order"]

            # Get only the last post content
            last_post_id = post_ids[0]

            # If last_post is unread, read and set this post as the last post
            if last_post_id != last_update_id: 
                last_update_id = last_post_id

                # Process post content. ProcessMessage(message, root_id)
                methods.processMessage(result["posts"][last_update_id]['message'], last_update_id)

        # Sleep for specified time
        time.sleep(config.TIMEOUT)

    except KeyboardInterrupt:
        print("Terminating Server")
        break