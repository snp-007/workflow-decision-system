import time


def retry(operation, retries=3):

    for i in range(retries):

        try:
            return operation()

        except Exception:

            if i == retries - 1:
                raise

            time.sleep(1)