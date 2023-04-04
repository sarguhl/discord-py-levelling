import re

def split_message(message: str, limit: int = 2000):
    """Splits a message into a list of messages if it exceeds limit.
    Messages are only split at new lines.
    Discord message limits:
        Normal message: 2000
        Embed description: 2048
        Embed field name: 256
        Embed field value: 1024"""
    if len(message) <= limit:
        return [message]
    else:
        lines = message.splitlines()
        new_message = ""
        message_list = []
        for line in lines:
            if len(new_message+line+"\n") <= limit:
                new_message += line+"\n"
            else:
                message_list.append(new_message)
                new_message = ""
        if new_message:
            message_list.append(new_message)
        return message_list 

def getEmojis(input: str):
    foundedEmojis = re.findall("<?(a)?:?(\w{2,32}):(\d{14,20})>", input)
    emojis = []
    json = [{"name": emoji[1], "id": str(emoji[2])} for emoji in foundedEmojis ]
    for emoji in json:
        if not emoji in emojis:
            emojis.append(emoji)
    return emojis


def shorten_text(text: str, *, length: int = 100, suffix: str = "...") -> str:
    """Kürzt einen bestimmten Text auf length. 
    Falls der Text ohne weiteres in die Länge passt, wird er direkt returned.
    Andernfalls wird er auf `length - len(suffix)` gekürzt und der Suffix wird angehängt.
    
    
    Parameters
    ----------
    text: `str`
        Text, welcher gekürzt werden soll
    length: `int = 100`
        Maximale Länge des neuen Texts
    suffix: `str = "..."`
        Zusätzlicher String welcher ans Ende vom gekürzten Text angehangen wird
    
    Returns
    -------
    `str`
        Den maximal length langen Text.
    """
    if len(text) > length:
        _ = text[: length - len(suffix)]
        text = _ + suffix
    return text