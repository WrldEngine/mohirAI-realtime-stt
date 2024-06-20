import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s-[%(levelname)s]: %(message)s"
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return logging