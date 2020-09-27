import string
import re

def replace(text):
    text = text.replace(">", "&gt;")
    text = text.replace("<", "&lt;")
    text = text.replace("&", "&amp;")

    return text

def checkViaRegex(text, regex):
    if(re.search(regex,text)):  
        return True
    else:  
        return False