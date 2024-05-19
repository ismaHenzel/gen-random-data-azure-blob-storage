import asyncio
import json
from argparse import ArgumentParser
from datetime import datetime

import httpx
import azure_blob_storage

# Parsing arguments
parser = ArgumentParser()
parser.add_argument("--container", type=str, help="container name to store random data")
parser.add_argument("--folder", type=str, help="folder name store random data inside container ")
parser.add_argument("--random_data_id", type=str, help="random data project id")
parser.add_argument("--random_data_key", type=str, help="random data project key")
parser.add_argument("--request_limit", type=int, help="simultaneous async requests value", default=1)
parser.add_argument(
    "--data_peer_batch",
    type=int,
    help="the number of random data to generate peer execution",
    default=10,
)
parser.add_argument(
    "--sleep_time",
    type=float,
    help="sleep time between requests to avoid blocking",
    default=2,
)
args = parser.parse_args()

random_data_project_id = args.random_data_id
random_data_project_key = args.random_data_key
random_data_peer_batch = args.data_peer_batch
random_data_request_limt = args.request_limit
random_data_request_sleep_time = args.sleep_time
azure_blob_container = args.container
azure_blob_folder = args.folder

if (not (azure_blob_container)) | (not (azure_blob_folder)):
    raise Exception("you shoud pass container and folder")

client = httpx.AsyncClient()
semaphore = asyncio.Semaphore(random_data_request_limt)


async def get_random_data(client: httpx.AsyncClient, project_id: str, project_key: str, sleep: int = None) -> dict:
    """
    Function that generates random data using the https://random-data-api.com/
    Args:
        client (httpx.AsyncClient): the current httpx async client
        project_id (str): the random-data project id
        project_key (str): the random-data key for the project
    """
    async with semaphore:
        url = f"https://random-data-api.com/api/v3/projects/{project_id}"
        response = await client.get(url, headers={"X-API-Key": project_key})
        if sleep:
            await asyncio.sleep(
                sleep
            )  # sleeping to not get blocked, you can remove if you don't have this kind of problem

        status_code = response.status_code
        print(f"random data - status code {status_code}")
        if status_code == 200:
            random_data = response.json()
            load_ts = int(datetime.now().timestamp())
            random_data.update({"load_ts": load_ts})
            return random_data


async def main() -> None:
    tasks = [
        get_random_data(
            client,
            random_data_project_id,
            random_data_project_key,
            random_data_request_sleep_time,
        )
        for i in range(random_data_peer_batch)
    ]
    random_data = await asyncio.gather(*tasks)
    load_ts = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    await azure_blob_storage.write_blob(
        container=azure_blob_container,
        filename=f"{azure_blob_folder}/{load_ts}.json",
        content=json.dumps(random_data),
    )
    await client.aclose()


asyncio.run(main())
