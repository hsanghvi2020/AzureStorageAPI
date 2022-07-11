# ---------------------------------------------------------------------------------------------------------
# Simple tutorial that demonstrates Azure Storage API. The following features are demonstrated:
# - Create a new container on specified Azure Storage Account
# - Creates a test file in user-specified folder on local system
# - Uploads test file to blob storage
# - Lists the blobs in the container
# - Downloads the blob with a new name
# ---------------------------------------------------------------------------------------------------------

import os
import uuid
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient, __version__


def run():
    print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")

    try:
        # Fetch connection string to Azure Storage Account from pre-defined OS Environment Variable
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        # Create the BlockBlobService that is used to call the Blob service for the storage account
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Attempt to create a new container. If container already exists, then fetch existing
        container_name = 'testcontainer'
        try:
            container_client = blob_service_client.create_container(container_name)
        except ResourceExistsError:
            print("Container already exists.")
            container_client = blob_service_client.get_container_client(container_name)

        # Create a working folder (if one not exists). Folder will be created in the local user's directory on system
        # (In Windows, C:\Users\<user_name>\AzureBlobStorage)
        local_path = os.path.expanduser("~/AzureBlobStorage")
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        # Create a new text file with a unique filename generated using UUID library
        local_file_name = "QuickStart_" + str(uuid.uuid4()) + ".txt"
        upload_file_path = os.path.join(local_path, local_file_name)

        # Write text to the file.
        file = open(upload_file_path, 'w')
        file.write("Hello, World! This is Harshil Sanghvi")
        file.close()

        print("Path to local text file = " + upload_file_path)
        print("\nUploading to Blob storage as blob " + local_file_name)

        # Upload the created file, use local_file_name for the blob name
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)

        # List the blobs in the container
        print("\nList blobs in the container")
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t Blob name: " + blob.name)

        # Download the blob
        # Add '_DOWNLOADED' as prefix to '.txt' so you can see both files in Documents.
        download_file_path = os.path.join(local_path, str.replace(local_file_name, '.txt', '_DOWNLOADED.txt'))
        print("\nDownloading blob to " + download_file_path)
        with open(download_file_path, "wb") as download_file:
            download_stream = blob_client.download_blob()
            download_file.write(download_stream.readall())

        # Uncomment below lines to run clean up code which deletes the created container,
        # deletes local files (both original and downloaded)
        # print("\nPress the Enter key to begin clean up")
        # input()

        # print("Deleting blob container...")
        # container_client.delete_container()

        # print("Deleting the local source and downloaded files...")
        # os.remove(upload_file_path)
        # os.remove(download_file_path)
        # os.rmdir(local_path)

        print("Done")
    except Exception as e:
        print(e)


# Main method.
if __name__ == '__main__':
    run()
