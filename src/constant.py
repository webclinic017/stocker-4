class Constant:

    """This is the constant class used in the application.
    Attributes:
        API_KEY (str): zerodha API key
        API_SECRET (str): Zerodha API secret
        CHROME_DRIVER_LOCATION (str): Chrome Driver Location Used for Selenium
        CLIENT_ID (str): Zerodha User ID
        CLIENT_PASSWORD (str): Zerodha Password
        DEPLOY_DIR (str): Data Dump Directory
        HOLIDA
        Y_DIR (str): Holiday List Directory
        LOGFILE_DIR (str): Logfile Directory
        TBOT_ID (str): Telegram Bot ID
        TBOT_TOKEN (str): Telegram Bot Token
        TOTP_KEY (str): TOTP key
    """

    # Directories - This needs to be changed when deployed in AWS
    DEPLOY_DIR = '/home/ubuntu/stocker/data'
    LOGFILE_DIR = '/home/ubuntu/stocker/logs'
    HOLIDAY_DIR = '/home/ubuntu/stocker/config/holidays.json'
    CHROME_DRIVER_LOCATION = '/usr/bin/chromedriver'

    # This section is for windows, will be commented in GITHUB , but later on this file will be added in gitignore
    #DEPLOY_DIR = 'D:\Projects\stocker\data'
    #LOGFILE_DIR = 'D:\Projects\stocker\logs'
    #HOLIDAY_DIR = 'D:\Projects\stocker\config\holidays.json'
    #CHROME_DRIVER_LOCATION = 'D:\Software\chromedriver\chromedriver.exe'

    # Zerodha Details
    API_KEY = 'yxrwphfcjpwe3104'
    API_SECRET = 'yi3xwwa6xbs36uz6i5o4h4cim2r5ab2e'
    CLIENT_ID = 'LH8735'
    CLIENT_PASSWORD = '78jBrna6Ycj&5SSE'
    TOTP_KEY = 'OBHYW6GF46XT2ZLMC5R57QUGDPDN2NGE'

    # Telegram
    TBOT_TOKEN = '5067002151:AAHpDvWf3LF6k-7egQJFHw3rjQe0fCJ43H0'
    TBOT_ID = '991843310'

    # db Details

    MASTER_KEY = 'BTrsTLzQkUEs0KRsybNr'
