from datetime import datetime
import pytz

def to_ist(dt: datetime) -> datetime:
    ist = pytz.timezone('Asia/Kolkata')
    return dt.astimezone(ist)
