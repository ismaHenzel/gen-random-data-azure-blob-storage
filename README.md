# Random Data Generator and Azure Blob Storage Uploader

This project contains a script that generates random data using the [Random Data API](https://random-data-api.com/) and uploads the generated data to Azure Blob Storage. The script supports asynchronous requests to fetch data in parallel and avoids API rate limiting by introducing configurable sleep intervals between requests.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/ismaHenzel/gen-random-data-azure-blob-storage
    cd random-data-azure-uploader
    ```

2. Install the required Python packages:

    ```bash
    poetry install
    ```
3. create the .env file:

    ```bash

    AZURE_BLOB_ACCOUNT_NAME=xxxxx
    AZURE_BLOB_ACCOUNT_URL=xxxx
    AZURE_BLOB_ACCOUNT_KEY=xxxx

    ```

## Usage

To run the script, use the following command:

```bash
python script.py --container CONTAINER_NAME --folder FOLDER_NAME --random_data_id RANDOM_DATA_PROJECT_ID --random_data_key RANDOM_DATA_PROJECT_KEY [--request_limit REQUEST_LIMIT] [--data_peer_batch DATA_PEER_BATCH] [--sleep_time SLEEP_TIME]

poetry run python3 gen_random_data.py --container=randomdata --folder=books --random_data_id=1cb243f3-43c5-49d6-ad1d-416503ae88ff --random_data_key=-KDs2atbyMRn3piJvGBHgQ --data_peer_batch=15 --sleep_time=1.5 --request_limit=1
```
