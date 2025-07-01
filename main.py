from datetime import datetime
from math import sin, cos, atan2, asin, radians
from timezonefinder import TimezoneFinder
from pytz import timezone, utc
tf = TimezoneFinder()

lat = 45.5355
lon = -73.761

JD_EPOCH = 2451545.0

def get_julian_date_number(year: int, month: int, day: int) -> float:
    """
    Calculate the Julian date number for a given date.

    Args:
        year (int): The year of the date.
        month (int): The month of the date. January is 1, December is 12.
        day (int): The day of the date.

    Returns:
        float: The Julian date number.
    """

    a = 1461 * (year + 4800 + (month - 14) / 12) / 4
    b = 367 * (month - 2 - (month - 14) / 12 * 12) / 12
    c = 3 * ((year + 4900 + (month - 14) / 12) / 100) / 4

    jd = a + b - c + day - 32075

    return jd
     
def get_equation_of_time_and_declination() -> tuple[float, float]:
    today = datetime.now()
    jdn = get_julian_date_number(today.year, today.month, today.day)
    d = jdn - JD_EPOCH
    g = 357.529 + 0.98560028* d
    q = 280.459 + 0.98564736* d
    L = q + 1.915* sin(radians(g)) + 0.020* sin(2*radians(g))
    R = 1.00014 - 0.01671* cos(radians(g)) - 0.00014* cos(2*radians(g))
    e = 23.439 - 0.00000036* d
    RA = atan2(cos(radians(e)) * sin(radians(L)), cos(radians(L)))/ 15

    # declination of the sun
    D = asin(sin(radians(e))* sin(radians(L)))
    # equation of time
    EqT = q/15 - RA
    

    return EqT, D

def get_timezone_offset_hours(lat: float, lon: float) -> float:
    today = datetime.now()

    tz_target = timezone(tf.certain_timezone_at(lng=lon, lat=lat))
    today_target = tz_target.localize(today)
    today_utc = utc.localize(today)

    return (today_utc - today_target).total_seconds() / 3600


def get_dhuhr_time(lat: float, lon: float) -> float:
    timezone_offset_hours = get_timezone_offset_hours(lat, lon)
    EqT, _= get_equation_of_time_and_declination()

    time = 12 + timezone_offset_hours - (lon / 15) - EqT

    return time



date = datetime.now()

year = date.year
month = date.month
day = date.day

formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
print("today is", formatted_date)

jd = get_julian_date_number(year, month, day)

print("julian date number is", jd)

print("timezone offset is", get_timezone_offset_hours(lat, lon))

print("dhuhr time is", get_dhuhr_time(lat, lon))



