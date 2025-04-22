from datetime import datetime, timedelta

def validate_rental_period(start_date: datetime, rental_days: int) -> bool:
    max_rental_days = 15
    if rental_days > max_rental_days:
        return False
    return True

def calculate_return_date(start_date: datetime, rental_days: int) -> datetime:
    return start_date + timedelta(days=rental_days)