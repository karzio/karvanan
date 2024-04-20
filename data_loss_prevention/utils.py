
def clean_timestamp(timestamp: str) -> int:
    """
    Timestamp from slack comes with a fraction of seconds.
    This is not needed and is stripped here.
    :param timestamp:
    :return: clean timestamp converted to int
    """
    ts = timestamp.split(".")[0]
    return int(ts)
