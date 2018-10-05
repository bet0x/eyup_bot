# Introduction
This Mattermost Bot procures information regarding uptime of the
server, disks usage, and users connected.

# Required packages

psutil => 5.4.7
```
pip install psutil
```

# Obtaining credentials from Mattermost

Obtain Session Token
```
curl -i -d '{"login_id":"abc@xyz.com","password":"password"}' http://<yourwebsite>.<com>/api/v4/users/login
```
---
Editing *config.py*

* Insert your SESSION_ID into Authorization field in header. 
* Input CHANNEL_ID in channel_id field.

# Running bot

Clone repository and cd into project repo. 
```
cd eyuptime_bot
```
Run daemon.
```
python daemon.py
```

# Usage

Running commands.
* -help
* -usage
* -disks
* -users

## Example
```
-help@eyup_bot
```