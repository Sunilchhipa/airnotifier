import requests
import random
from api import API_PERMISSIONS

HUBURL = "https://moodle.net/local/sitecheck/check.php"


def process_pushnotification_payload(data):
    extra = data.get("extra", {})
    userfrom = extra.get("userfromfullname", None)
    usertoid = extra.get("usertoid", None)
    site = extra.get("site", None)
    timecreated = extra.get("timecreated", None)
    message = extra.get("smallmessage", None)
    notif = extra.get("notification", None)
    title = extra.get("sitefullname", None)
    component = extra.get("component", '')
    name = extra.get("name", '')
    wwwroot = extra.get("wwwroot", '')
    conversationtype = extra.get("conversationtype", '')
    courseid = extra.get("courseid", '')
    contexturl = extra.get("contexturl", '')

    if not message:
        message = extra.get("fullmessage", None)

    if not title:
        title = "Notification"

    # Set the correct device.
    device = data.get('device', None).lower()
    if device == "android-fcm" or device == "ios-fcm":
        data["device"] = "fcm"

    data["gcm"] = {
        "data": {
            "title": title,
            "site": site,
            "userfrom": userfrom,
            "usertoid": usertoid,
            "notif": notif,
            "notId": random.randint(1, 1000000),
            "component": component,
            "name": name,
            "wwwroot": wwwroot,
            "conversationtype": conversationtype,
            "courseid": courseid,
            "contexturl": contexturl,
        }
    }

    data["apns"] = {
        "custom": {
            "title": title,
            "site": site,
            "userfrom": userfrom,
            "usertoid": usertoid,
            "notif": notif,
            "component": component,
            "name": name,
            "wwwroot": wwwroot,
            "conversationtype": conversationtype,
            "courseid": courseid,
            "contexturl": contexturl,
        }
    }

    # Payload for the fcm notifications
    data["fcm"] = {
        "android": {
            "data": {
                "sound": "default",
                "body": message,
                "title": '',
                "site": site,
                "userfrom": userfrom,
                "usertoid": usertoid,
                "android_channel_id": "PushPluginChannel",
                "notId": str(random.randint(1, 1000000)),
                "notif": notif,
                "component": component,
                "name": name,
                "wwwroot": wwwroot,
                "conversationtype": conversationtype,
                "courseid": courseid,
                "contexturl": contexturl,
            },
            "priority": "high",
        },
        "apns": {
            "payload": {
                "aps": {
                    "sound": "default",
                    "alert": {
                        "body": message,
                        "title": '',
                        "site": site,
                        "userfrom": userfrom,
                        "usertoid": usertoid,
                        "notif": notif,
                        "component": component,
                        "name": name,
                        "wwwroot": wwwroot,
                        "conversationtype": conversationtype,
                        "courseid": courseid,
                        "contexturl": contexturl,
                    }
                }
            }
        }
    }

    if "alert" not in data:
        data["alert"] = {"body": message, "title": title}

    if not "wns" in extra:
        data["extra"]["wns"] = {
            "type": "toast",
            "template": "ToastText01",
            "text": [data["alert"]],
        }

    if not "fcm" in extra:
        data["extra"]["fcm"] = {"fcm-message": "this is fcm hook"}

    return data


def process_accesskey_payload(data):
    mdlurl = data.get("url", "")
    mdlsiteid = data.get("siteid", "")
    params = {"siteid": mdlsiteid, "url": mdlurl}
    response = requests.get(HUBURL, params=params)
    result = int(response.text)
    if result == 0:
        raise Exception("Site not registered on moodle.net")
    else:
        # This is 1111 in binary means all permissions are granted
        data["permission"] = (
            API_PERMISSIONS["create_token"][0]
            | API_PERMISSIONS["delete_token"][0]
            | API_PERMISSIONS["send_notification"][0]
            | API_PERMISSIONS["send_broadcast"][0]
        )
        return data

def process_token_payload(data):
    return data
