import requests
from azure.storage.blob import BlockBlobService, PublicAccess, ContentSettings

#Enter details of Azure Blob Storage Container Here
storageAccountName = "<your-storage-account-name>"
storageKey = "<your-storage-key>"
storageContainer = "<your-storage-container-name>"


dummyDict = {"imageURL": "None", "imagePath": "None"}

def uploadBlob(filePath, blobName):

    bbs = BlockBlobService(account_name=storageAccountName, account_key=storageKey)
    bbs.create_blob_from_path(container_name=storageContainer,blob_name=blobName, file_path=filePath, content_settings=ContentSettings(content_type='image/jpg'))
    imageURL = "https://{0}.blob.core.windows.net/{1}/{2}".format(storageAccountName, storageContainer, blobName)
    imagePath = "{0}/{1}".format(storageContainer, blobName)
    returnDict = {"imageURL": imageURL, "imagePath": imagePath}
    return returnDict
