class Constant:

    """This is the constant class used in the application.


    Attributes:
        API_KEY (str): zerodha API key
        API_SECRET (str): Zerodha API secret
        CHROME_DRIVER_LOCATION (str): Chrome Driver Location Used for Selenium
        CLIENT_ID (str): Zerodha User ID
        CLIENT_PASSWORD (str): Zerodha Password
        DEPLOY_DIR (str): Data Dump Directory
        HOLIDAY_DIR (str): Holiday List Directory
        LOGFILE_DIR (str): Logfile Directory
        TBOT_ID (str): Telegram Bot ID
        TBOT_TOKEN (str): Telegram Bot Token
        TOTP_KEY (str): TOTP key
    """

    # Directories - This needs to be changed when deployed in AWS
    DEPLOY_DIR = '/home/ubuntu/stockerApp/freedom/data'
    LOGFILE_DIR = '/home/ubuntu/stockerApp/freedom/logs'
    HOLIDAY_DIR = '/home/ubuntu/stockerApp/freedom/config/holidays.json'
    CHROME_DRIVER_LOCATION = '/usr/bin/chromedriver'

    # Zerodha Details
    API_KEY = 'yxrwphfcjpwe3104'
    API_SECRET = 'yi3xwwa6xbs36uz6i5o4h4cim2r5ab2e'
    CLIENT_ID = 'LH8735'
    CLIENT_PASSWORD = '78jBrna6Ycj&5SSE'
    TOTP_KEY = 'OBHYW6GF46XT2ZLMC5R57QUGDPDN2NGE'

    # Telegram
    TBOT_TOKEN = '5067002151:AAHpDvWf3LF6k-7egQJFHw3rjQe0fCJ43H0'
    TBOT_ID = '991843310'
