import datetime
import pytz


def tzware_datetime():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    return datetime.datetime.now(pytz.timezone('Asia/Calcutta'))

def current_date():
    return datetime.datetime.today().strftime("%m-%Y-%d")

def timedelta_months(months, compare_date=None):
    """
    Return a new datetime with a month offset applied.

    :param months: Amount of months to offset
    :type months: int
    :param compare_date: Date to compare at
    :type compare_date: date
    :return: datetime
    """
    if compare_date is None:
        compare_date = datetime.date.today()

    delta = months * 365 / 12
    compare_date_with_delta = compare_date + datetime.timedelta(delta)

    return compare_date_with_delta

def expired_order(expiry_date=None):
    if expiry_date is None:
        return None
    # print('EXPIRY DATE IS: ', expiry_date)
    # print('EXPIRY DATE TYPE IS: ', type(expiry_date))
    
    tz_info = expiry_date.tzinfo
    what_is_today = datetime.datetime.now(tz_info)
    # print('TODAY IS: ', what_is_today)
    # print('TODAY TYPE IS: ', type(what_is_today))
    if expiry_date < what_is_today:
        return True
    else:
        return False