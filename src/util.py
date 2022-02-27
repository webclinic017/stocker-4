
import calendar
import json
import logging
import math
import time
import urllib.request
from datetime import datetime, timedelta, date

from constant import Constant

DATE_FORMAT = "%Y%m%d"


def get_monthly_expiry_day_date(datetime_obj=None):
    """This Method calculates the Monthly Expriy Date

    Args:
        datetime_obj (None, optional): Sysdate or Any other date,optional

    Returns:
        datetime: Returns Monthly Expriy Date
    """
    if datetime_obj is None:
        datetime_obj = datetime.now()
    year = datetime_obj.year
    month = datetime_obj.month
    # 2nd entry is the last day of the month
    last_day = calendar.monthrange(year, month)[1]
    datetime_expiry_day = datetime(year, month, last_day)
    while calendar.day_name[datetime_expiry_day.weekday()] != 'Thursday':
        datetime_expiry_day = datetime_expiry_day - timedelta(days=1)
    while is_holiday(datetime_expiry_day):
        datetime_expiry_day = datetime_expiry_day - timedelta(days=1)

    datetime_expiry_day = get_time_of_day(0, 0, 0, datetime_expiry_day)
    return datetime_expiry_day


def prepare_weekly_options_symbol(input_symbol,  # pylint: disable-msg=too-many-locals
                                  strike,
                                  option_type,
                                  num_weeks_plus=0):
    """<FRESHLY_INSERTED>"""
    expiry_date_time = get_weekly_expiry_day_date()
    today_market_start_time = get_market_start_time()
    expiry_day_market_end_time = get_market_end_time(expiry_date_time)
    if num_weeks_plus > 0:
        expiry_date_time = expiry_date_time + \
            timedelta(days=num_weeks_plus * 7)
        expiry_date_time = get_weekly_expiry_day_date(expiry_date_time)
    if today_market_start_time > expiry_day_market_end_time:
        expiry_date_time = expiry_date_time + timedelta(days=6)
        expiry_date_time = get_weekly_expiry_day_date(expiry_date_time)
    # Check if monthly and weekly expiry same
    expiry_date_time_monthly = get_monthly_expiry_day_date()
    week_and_month_expriy_same = False
    if expiry_date_time == expiry_date_time_monthly:
        week_and_month_expriy_same = True
        logging.info('Weekly and Monthly expiry is same for %s',
                     expiry_date_time)
    year2_digits = str(expiry_date_time.year)[2:]
    option_symbol = None
    if week_and_month_expriy_same:
        month_short = calendar.month_name[expiry_date_time.month].upper()[0:3]
        option_symbol = input_symbol \
            + str(year2_digits) \
            + month_short \
            + str(strike) \
            + option_type.upper()
    else:
        mon = expiry_date_time.month
        day_var = expiry_date_time.day
        m_str = str(mon)
        if mon == 10:
            m_str = "O"
        elif mon == 11:
            m_str = "N"
        elif mon == 12:
            m_str = "D"
        d_str = ("0" + str(day_var)) if day_var < 10 else str(day_var)
        option_symbol = input_symbol \
            + str(year2_digits) \
            + m_str + d_str \
            + str(strike) \
            + option_type.upper()
    logging.info('prepare_weekly_options_symbol[%s, %d, %s, %d] = %s',
                 input_symbol,
                 int(strike),
                 option_type,
                 num_weeks_plus,
                 option_symbol)
    return option_symbol


def wait_until(hour, minute, seconds=0):
    """Summary

    Args:
        hour (TYPE): Description
        minute (TYPE): Description
        seconds (int, optional): Description

    Returns:
        TYPE: Description
    """
    today = date.today()
    end_datetime = datetime(today.year, today.month,
                            today.day, hour, minute, seconds)
    while True:
        wait_seconds = (end_datetime - datetime.now()).total_seconds()

        if wait_seconds < 0:
            return  # In case end_datetime was in past to begin with
        logging.info("Waiting for %d seconds as per strategy...",
                     wait_seconds / 2)
        time.sleep(wait_seconds / 2)
        if wait_seconds <= 0.1:
            return


def get_market_start_time(date_time_obj=None):
    """Summary

    Args:
        date_time_obj (None, optional): Description

    Returns:
        TYPE: Description
    """
    return get_time_of_day(9, 15, 0, date_time_obj)


def get_time_of_day(hours, minutes, seconds, date_time_obj=None):
    """Summary

    Args:
        hours (TYPE): Description
        minutes (TYPE): Description
        seconds (TYPE): Description
        date_time_obj (None, optional): Description

    Returns:
        TYPE: Description
    """
    if date_time_obj is None:
        date_time_obj = datetime.now()
    date_time_obj = date_time_obj.replace(
        hour=hours, minute=minutes, second=seconds, microsecond=0)
    return date_time_obj


def get_weekly_expiry_day_date(date_time_obj=None):
    """Summary

    Args:
        date_time_obj (None, optional): Description

    Returns:
        TYPE: Description
    """
    if date_time_obj is None:
        date_time_obj = datetime.now()
    days_to_add = 0
    if date_time_obj.weekday() >= 3:
        days_to_add = -1 * (date_time_obj.weekday() - 3)
    else:
        days_to_add = 3 - date_time_obj.weekday()
    datetime_expiry_day = date_time_obj + timedelta(days=days_to_add)
    while is_holiday(datetime_expiry_day):
        datetime_expiry_day = datetime_expiry_day - timedelta(days=1)

    datetime_expiry_day = get_time_of_day(0, 0, 0, datetime_expiry_day)
    return datetime_expiry_day


def publish_status(program_name, status):
    """Summary

    Args:
        program_name (TYPE): Description
        status (TYPE): Description
    """
    logging.info('Publishing Status to Healthcheck.io')
    if program_name == Constant.PROGRAM_NAME_ALPHA:
        if status:
            urllib.request.urlopen(  # pylint: disable-msg=consider-using-with
                Constant.ALPHA_STATUS_OK, timeout=10)
        else:
            urllib.request.urlopen(  # pylint: disable-msg=consider-using-with
                Constant.ALPHA_STATUS_FAIL, timeout=10)


def get_curr_date_str():
    """Summary

    Returns:
        TYPE: Description
    """
    return convert_to_date_str(datetime.now())


def convert_to_date_str(datetime_obj):
    """Summary

    Args:
        datetime_obj (TYPE): Description

    Returns:
        TYPE: Description
    """
    return datetime_obj.strftime(DATE_FORMAT)


def is_today_holiday():
    """Summary

    Returns:
        TYPE: Description
    """
    return is_holiday(datetime.now())


def is_holiday(datetime_obj):
    """Summary

    Args:
        datetime_obj (TYPE): Description

    Returns:
        TYPE: Description
    """
    date_str = convert_to_date_str(datetime_obj)
    with open(Constant.HOLIDAY_DIR, 'r', encoding='utf-8') as holidays:
        holidays_data = json.load(holidays)
    if date_str not in holidays_data:
        return False

    return True


def round_to_nse_price(price):
    """Summary

    Args:
        price (TYPE): Description

    Returns:
        TYPE: Description
    """
    var_1 = round(price, 2) * 20
    var_2 = math.ceil(var_1)
    return var_2 / 20


def get_epoch(datetime_obj=None):
    """Summary

    Args:
        datetime_obj (None, optional): Description

    Returns:
        TYPE: Description
    """
    if datetime_obj is None:
        datetime_obj = datetime.now()
    epoch_seconds = datetime.timestamp(datetime_obj)
    return int(epoch_seconds)  # converting double to long


def prepare_monthly_expiry_futures_symbol(input_symbol):
    """Summary

    Args:
        input_symbol (TYPE): Description

    Returns:
        TYPE: Description
    """
    expiry_date_time = get_monthly_expiry_day_date()
    expiry_date_market_end_time = get_market_end_time(expiry_date_time)
    now = datetime.now()
    if now > expiry_date_market_end_time:
        # increasing today date by 20 days to get some
        # day in next month passing to get_monthly_expiry_day_date()
        expiry_date_time = get_monthly_expiry_day_date(
            now + timedelta(days=20))
    year2_digits = str(expiry_date_time.year)[2:]
    month_short = calendar.month_name[expiry_date_time.month].upper()[0:3]
    future_symbol = input_symbol + year2_digits + month_short + 'FUT'
    logging.info(
        'prepare_monthly_expiry_futures_symbol[%s] = %s', input_symbol, future_symbol)
    return future_symbol


def get_market_end_time(date_time_obj=None):
    """Summary

    Args:
        date_time_obj (None, optional): Description

    Returns:
        TYPE: Description
    """
    return get_time_of_day(15, 30, 0, date_time_obj)
