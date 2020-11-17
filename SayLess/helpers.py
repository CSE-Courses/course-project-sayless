import os
import string
import re

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from emoji import UNICODE_EMOJI

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

def get_secret(secretName):
    KVUri = f"https://sayless.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)

    retrieved_secret = client.get_secret(secretName)

    return retrieved_secret.value

def is_emoji(s):
    count = 0
    for emoji in UNICODE_EMOJI:
        count += s.count(emoji)
        if count > 1:
            return False
    return bool(count)