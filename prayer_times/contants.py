 # Constants for all items the times are computed for
IMSAK = 'Imsak'
FAJR = 'Fajr'
SUNRISE = 'Sunrise'
ZHUHR = 'Dhuhr'
ASR = 'Asr'
SUNSET = 'Sunset'
MAGHRIB = 'Maghrib'
ISHA = 'Isha'
MIDNIGHT = 'Midnight'
FIRST_THIRD = 'Firstthird'
LAST_THIRD = 'Lastthird'

# Schools that determine the Asr shadow
SCHOOL_STANDARD = 'STANDARD'
SCHOOL_HANAFI = 'HANAFI'

# Midnight Mode - how the midnight time is determined
MIDNIGHT_MODE_STANDARD = 'STANDARD'
MIDNIGHT_MODE_JAFARI = 'JAFARI'

# Higher Latitude Adjustment Methods
LATITUDE_ADJUSTMENT_METHOD_MOTN = 'MIDDLE_OF_THE_NIGHT'
LATITUDE_ADJUSTMENT_METHOD_ANGLE = 'ANGLE_BASED'
LATITUDE_ADJUSTMENT_METHOD_ONESEVENTH = 'ONE_SEVENTH'
LATITUDE_ADJUSTMENT_METHOD_NONE = 'NONE'

# Formats in which data can be output
TIME_FORMAT_24H = '24h'
TIME_FORMAT_12H = '12h'
TIME_FORMAT_12hNS = '12hNS'
TIME_FORMAT_FLOAT = 'Float'
TIME_FORMAT_ISO8601 = 'iso8601'

# If we're unable to calculate a time, we'll return this
INVALID_TIME = '-----'