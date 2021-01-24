import re

# ? All valid characters, reserved and unreserved in a url
urlValidChars = r"[a-z0-9\-_~\/:\?#\[\]@!$&\'\(\)\*+,;=]"

urlregex = re.compile(
    r"(\"|'|`)"  # * Here to only pick up strings
    r"((http|https)://)?"  # ? Check for http/https ("https://xxx.xxx")
    # ? Check for main url segment ("maindomain.xxx")
    rf"([a-z0-9]{urlValidChars}*)"
    # ? Check for suburl segments ("xxx.sub.domain")
    rf"(\.{urlValidChars}+)+"
    r"(\"|'|`)"  # * Here to only pick up strings
)