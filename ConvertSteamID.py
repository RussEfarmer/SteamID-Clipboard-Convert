import clipboard
import re
text = clipboard.paste()

#Gets the stuff we want
def getimportanttext(text):
    text = str.lower(text)
    urlmatch = re.compile("https?://(?:www\.)?steamcommunity.com/profiles/[0-9]*")
    idmatch = re.compile("steam_0:[0-1]:[0-9]*")
    urls = urlmatch.findall(text)
    ids = idmatch.findall(text)
    return {"URL":urls, "ID":ids}

#Converts steamid64 to steamid32 with ghetto binary math
def tosteamid(text):
    idmatch = re.compile("[0-9]*$")
    id = int(idmatch.findall(text)[0])
    y_mask = int("1", base=2)
    z_mask = int("1111111111111111111111111111110", base=2)
    y = id & y_mask
    z = id & z_mask
    return f"STEAM_0:{y}:{int(z/2)}"

#Converts steamid32 to a community profile URL
def tourl(text):
    #Default account identifier for standard steam accounts
    acc_identifier = 76561197960265728
    parts = text.split(":")
    steam64id = int(parts[2])*2+int(parts[1])+acc_identifier
    return "https://steamcommunity.com/profiles/" + str(steam64id)

#Conversion logic
def convert(results):
    if not results:
        raise ValueError("No arguments")
    
    elif not isinstance(results, dict):
        raise TypeError("Not a dictionary")

    elif not results["URL"] and not results["ID"]:
        raise Exception("Input contains no usable data")

    elif results["URL"] and not results["ID"]:
        text_out = ""
        for i in results["URL"]:
            text_out = text_out + tosteamid(i) + "\n"
        return text_out

    elif results["ID"] and not results["URL"]:
        text_out = ""
        for i in results["ID"]:
            text_out = text_out + tourl(i) + "\n"
        return text_out

    elif results["ID"] and results["URL"]:
        text_id = "-=IDs converted to URLs=-\n"
        for i in results["ID"]:
            text_id = text_id + f"{i.upper()}: {tourl(i)}\n"
        text_url = "\n-=URLs converted to IDs=-\n"
        for i in results["URL"]:
            text_url = text_url + f"{i}: {tosteamid(i)}\n"
        return text_id + text_url
    else:
        raise Exception("Processing error")

clipboard.copy(convert(getimportanttext(text)))