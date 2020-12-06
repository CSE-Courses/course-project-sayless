import os
import string
import re

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContentSettings
from emoji import UNICODE_EMOJI

def create_container_sample(container_name):
    # Instantiate a new ContainerClient
    container_client = blob_service_client.get_container_client(container_name)

    try:
        # Create new container in the service
        container_client.create_container()

        return True
    
    except:
        return False

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

# Instantiate a new BlobServiceClient using a connection string
connection_string = get_secret("Image")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def is_emoji(s):
    count = 0
    for emoji in UNICODE_EMOJI:
        count += s.count(emoji)
        if count > 1:
            return False
    return bool(count)