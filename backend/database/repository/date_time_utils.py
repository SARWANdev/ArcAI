from datetime import datetime, UTC

def get_utc_zulu_timestamp() -> str:
    """
    Returns current UTC time in ISO 8601 format with 'Z' suffix.
    """
    return datetime.now(UTC).isoformat(timespec='seconds').replace('+00:00', 'Z')