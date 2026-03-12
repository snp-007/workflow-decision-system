import time


def retry_operation(operation, retries=3, delay=1):

    for attempt in range(retries):

        try:
            return operation()

        except Exception as e:

            if attempt == retries - 1:
                raise e

            time.sleep(delay)