import json
import logging
import os

import util
from constant import Constant
from datetime import datetime, timedelta, date


def fetch_instrument_from_server(kite):
    """Summary

    Args:
        kite (TYPE): Description

    Returns:
        TYPE: Description
    """
    return kite.instruments('NFO')


def cleanup_instrumnet(instruments):
    """Summary

    Args:
        instruments (TYPE): Description

    Returns:
        TYPE: Description
    """
    monthly_expiry = util.get_monthly_expiry_day_date()
    monthly_expiry = monthly_expiry.date()
    weekly_expiry = util.get_weekly_expiry_day_date()
    weekly_expiry = weekly_expiry.date()
    logging.info(monthly_expiry)
    logging.info(weekly_expiry)
    res_istruments = [i for i in instruments if (
        i['expiry'] == monthly_expiry or i['expiry'] == weekly_expiry)]
    return res_istruments


def get_instrument(kite):
    """Summary

    Args:
        kite (TYPE): Description

    Returns:
        TYPE: Description
    """
    return cleanup_instrumnet(fetch_instrument_from_server(kite))


def save_instrument(instruments):
    """Summary

    Args:
        instruments (TYPE): Description
    """
    instruments_filepath = os.path.join(
        Constant.DEPLOY_DIR, 'instruments.json')
    with open(instruments_filepath, 'w', encoding='utf-8') as isd_file:
        json.dump(instruments, isd_file, indent=2, default=str)
    logging.info('Instruments: Saved %d instruments to file %s',
                 len(instruments), instruments_filepath)


def get_instrument_all(kite):
    """Summary

    Args:
        kite (TYPE): Description
    """
    save_instrument(get_instrument(kite))
