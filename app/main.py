import time
import os
from dotenv import load_dotenv
from api_session import open_session, close_session
from api_expose import start_prometheus, concurrent_requests, time_script
from loguru import logger 

load_dotenv()
start_prometheus()

while True:
    headers = None
    try:
        start_time = time.time()
        headers = open_session()
        if headers is None:
            logger.info("Failed to open session after maximum attempts, stopping...")
            continue
        concurrent_requests(headers)
        time_script(start_time)

    finally:
        if headers is not None:
            close_response = close_session(headers)
            if "success" in close_response and close_response["success"]:
                logger.info("Session close: Success")
                logger.info("------")
                time.sleep(int(os.getenv("SCRAPE_INTERVAL")))
            else:
                logger.error("Session close: Fail")
                logger.error(close_response)
                logger.error("------")
        elif headers is None:
            logger.info("------")
            time.sleep(int(os.getenv("SCRAPE_INTERVAL")))
