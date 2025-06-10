from datetime import datetime


def audit_log_transaction(tourist_id: str, message: str = "") -> None:
    with open("audit_log.txt", mode="a", encoding="utf-8") as logfile:
        content = f"tourist {tourist_id} executed {message} at {datetime.now()}"
        logfile.write(content)
