"""
Main PrayerTimes class for calculating Islamic prayer times.
"""

import datetime
import math
from typing import Dict, Any, Optional, Union
from prayer_times.method import Method
from prayer_times.dmath import DMath
from prayer_times.contants import *

class PrayerTimes:
    """Main class for calculating Islamic prayer times."""
    
   

    
    def __init__(self, method=Method.METHOD_MWL, school=SCHOOL_STANDARD, asr_shadow_factor=None):
        """Initialize PrayerTimes with method and settings."""
        self.methods = {}
        self.method_codes = []
        self.date = None
        self.method = method
        self.school = school
        self.midnight_mode = MIDNIGHT_MODE_STANDARD
        self.latitude_adjustment_method = LATITUDE_ADJUSTMENT_METHOD_ANGLE
        self.time_format = TIME_FORMAT_24H
        self.latitude = None
        self.longitude = None
        self.elevation = None
        self.asr_shadow_factor = asr_shadow_factor
        self.settings = None
        self.shafaq = 'general'  # Only valid for METHOD_MOONSIGHTING
        self.offset = {}
        
        self.load_methods()
        self.set_method(method)
        self.set_school(school)
        if asr_shadow_factor is not None:
            self.asr_shadow_factor = asr_shadow_factor
        self.load_settings()
    
    def set_shafaq(self, shafaq: str):
        """Set the shafaq parameter for moonsighting method."""
        self.shafaq = shafaq
    
    def set_custom_method(self, method: Method):
        """Set a custom calculation method."""
        self.set_method(Method.METHOD_CUSTOM)
        self.methods[self.method] = method.__dict__
        self.load_settings()
    
    def load_settings(self):
        """Load settings based on the current method."""
        self.settings = type('Settings', (), {})()
        
        self.settings.Imsak = self.methods[self.method].get('params', {}).get(IMSAK, '10 min')
        self.settings.Fajr = self.methods[self.method].get('params', {}).get(FAJR, 0)
        self.settings.Dhuhr = self.methods[self.method].get('params', {}).get(ZHUHR, '0 min')
        self.settings.Isha = self.methods[self.method].get('params', {}).get(ISHA, 0)
        self.settings.Maghrib = self.methods[self.method].get('params', {}).get(MAGHRIB, '0 min')
        
        # Pick up methods midnightMode
        if (self.methods[self.method].get('params', {}).get(MIDNIGHT) == 
            MIDNIGHT_MODE_JAFARI):
            self.set_midnight_mode(MIDNIGHT_MODE_JAFARI)
        else:
            self.set_midnight_mode(MIDNIGHT_MODE_STANDARD)
    
    def get_times_for_today(self, latitude: float, longitude: float, date: datetime.datetime, 
                           elevation: Optional[float] = None, 
                           latitude_adjustment_method: str = LATITUDE_ADJUSTMENT_METHOD_ANGLE,
                           midnight_mode: Optional[str] = None, 
                           format: str = TIME_FORMAT_24H) -> Dict[str, Any]:
        """Get prayer times for today."""
        return self.get_times(date, latitude, longitude, elevation, 
                             latitude_adjustment_method, midnight_mode, format)
    
    def get_times(self, date: datetime.datetime, latitude: float, longitude: float,
                  elevation: Optional[float] = None,
                  latitude_adjustment_method: str = LATITUDE_ADJUSTMENT_METHOD_ANGLE,
                  midnight_mode: Optional[str] = None,
                  format: str = TIME_FORMAT_24H):
        """Get prayer times for a specific date."""
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.elevation = 0 if elevation is None else float(elevation)
        self.set_time_format(format)
        self.set_latitude_adjustment_method(latitude_adjustment_method)
        if midnight_mode is not None:
            self.set_midnight_mode(midnight_mode)
        self.date = date
        
        return self.compute_times()
    
    def compute_times(self):
        """Compute all prayer times."""
        # default times
        times = {
            IMSAK: 5,
            FAJR: 5,
            SUNRISE: 6,
            ZHUHR: 12,
            ASR: 13,
            SUNSET: 18,
            MAGHRIB: 18,
            ISHA: 18
        }
        
        times = self.compute_prayer_times(times)
        times = self.adjust_times(times)
        
        # add night times
        if self.midnight_mode == MIDNIGHT_MODE_JAFARI:
            diff = self.time_diff(times[SUNSET], times[FAJR])
        else:
            diff = self.time_diff(times[SUNSET], times[SUNRISE])
        
        times[MIDNIGHT] = times[SUNSET] + diff / 2
        times[FIRST_THIRD] = times[SUNSET] + diff / 3
        times[LAST_THIRD] = times[SUNSET] + 2 * (diff / 3)
        
        # If our method is Moonsighting, reset the Fajr and Isha times
        if self.method == Method.METHOD_MOONSIGHTING:
            times = self.moonsighting_recalculation(times)
        
        times = self.tune_times(times)
        
        return self.modify_formats(times)
    
    def moonsighting_recalculation(self, times: Dict[str, float]) -> Dict[str, float]:
        """Recalculate Fajr and Isha times for moonsighting method."""
        # Note: This is a simplified version. The full implementation would require
        # the moonsighting calculation classes which are not included in the original PHP
        # For now, we'll use standard calculations
        return times
    
    def modify_formats(self, times: Dict[str, float]) -> Dict[str, Union[str, float]]:
        """Modify time formats based on the specified format."""
        result: Dict[str, Union[str, float]] = {}
        for prayer, time in times.items():
            result[prayer] = self.get_formatted_time(time, self.time_format, prayer)
        return result
    
    def get_formatted_time(self, time: float, format: str, prayer: str) -> Union[str, float]:
        """Format time according to the specified format."""
        if math.isnan(time):
            return self.INVALID_TIME
        
        if format == TIME_FORMAT_FLOAT:
            return time
        
        suffixes = ['am', 'pm']
        
        time = time + 0.5 / 60  # add 0.5 minutes for rounding
        fix_time = DMath.fix_hour(time)  # wrap to 00h-23h
        
        hours = int(fix_time)
        minutes = int((fix_time - hours) * 60)
        
        if self.time_format == TIME_FORMAT_12H:
            suffix = suffixes[0] if hours < 12 else suffixes[1]
        else:
            suffix = ''
        
        if format == TIME_FORMAT_24H:
            hour = f"{hours:02d}"
        else:
            hour = str(((hours + 12 - 1) % 12) + 1)
        
        two_digit_minutes = f"{minutes:02d}"
        
        if format == TIME_FORMAT_ISO8601:
            # Create temporary date object
            temp_date = self.date.replace(hour=0, minute=0, second=0, microsecond=0)
            if time > 0:
                temp_date += datetime.timedelta(minutes=int(time * 60))
            else:
                temp_date -= datetime.timedelta(minutes=int(-time * 60))
            return temp_date.isoformat()
        
        return f"{hour}:{two_digit_minutes}{' ' + suffix if suffix else ''}"
    
    def tune_times(self, times: Dict[str, float]) -> Dict[str, float]:
        """Apply time offsets."""
        if self.offset:
            for prayer, time in times.items():
                if prayer in self.offset:
                    times[prayer] += self.offset[prayer] / 60
        return times
    
    def evaluate(self, value: Union[str, float]) -> float:
        """Evaluate a string or numeric value."""
        if isinstance(value, str):
            # Remove non-numeric characters and convert to float
            import re
            numeric_part = re.sub(r'[^\d.-]', '', value)
            return float(numeric_part) if numeric_part else 0.0
        return float(value)
    
    def adjust_times(self, times: Dict[str, float]) -> Dict[str, float]:
        """Adjust times for timezone and other factors."""
        # Get timezone offset in hours
        if self.date.tzinfo:
            tz_offset = self.date.utcoffset().total_seconds() / 3600
        else:
            tz_offset = 0
        
        for prayer in times:
            times[prayer] += (tz_offset - self.longitude / 15)
        
        if self.latitude_adjustment_method != LATITUDE_ADJUSTMENT_METHOD_NONE:
            times = self.adjust_high_latitudes(times)
        
        if self.is_min(self.settings.Imsak):
            times[IMSAK] = times[FAJR] - self.evaluate(self.settings.Imsak) / 60
        
        if self.is_min(self.settings.Maghrib):
            times[MAGHRIB] = times[SUNSET] + self.evaluate(self.settings.Maghrib) / 60
        
        if self.is_min(self.settings.Isha):
            times[ISHA] = times[MAGHRIB] + self.evaluate(self.settings.Isha) / 60
        
        times[ZHUHR] += self.evaluate(self.settings.Dhuhr) / 60
        
        return times
    
    def adjust_high_latitudes(self, times: Dict[str, float]) -> Dict[str, float]:
        """Adjust times for high latitude regions."""
        night_time = self.time_diff(times[SUNSET], times[SUNRISE])
        
        times[IMSAK] = self.adjust_hl_time(
            times[IMSAK], times[SUNRISE], 
            self.evaluate(self.settings.Imsak), night_time, 'ccw'
        )
        times[FAJR] = self.adjust_hl_time(
            times[FAJR], times[SUNRISE], 
            self.evaluate(self.settings.Fajr), night_time, 'ccw'
        )
        times[ISHA] = self.adjust_hl_time(
            times[ISHA], times[SUNSET], 
            self.evaluate(self.settings.Isha), night_time
        )
        times[MAGHRIB] = self.adjust_hl_time(
            times[MAGHRIB], times[SUNSET], 
            self.evaluate(self.settings.Maghrib), night_time
        )
        
        return times
    
    def is_min(self, value: Union[str, float]) -> bool:
        """Check if the value contains 'min' indicating minutes."""
        if isinstance(value, str):
            return 'min' in value
        return False
    
    def adjust_hl_time(self, time: float, base: float, angle: float, 
                      night: float, direction: Optional[str] = None) -> float:
        """Adjust time for high latitude regions."""
        portion = self.night_portion(angle, night)
        if direction == 'ccw':
            time_diff = self.time_diff(time, base)
        else:
            time_diff = self.time_diff(base, time)
        
        if math.isnan(time) or time_diff > portion:
            if direction == 'ccw':
                time = base - portion
            else:
                time = base + portion
        
        return time
    
    def night_portion(self, angle: float, night: float) -> float:
        """Calculate night portion based on adjustment method."""
        method = self.latitude_adjustment_method
        portion = 1/2  # MidNight
        
        if method == LATITUDE_ADJUSTMENT_METHOD_ANGLE:
            portion = 1/60 * angle
        elif method == LATITUDE_ADJUSTMENT_METHOD_ONESEVENTH:
            portion = 1/7
        
        return portion * night
    
    def time_diff(self, t1: float, t2: float) -> float:
        """Calculate time difference between two times."""
        return DMath.fix_hour(t2 - t1)
    
    def compute_prayer_times(self, times: Dict[str, float]) -> Dict[str, float]:
        """Compute prayer times using astronomical calculations."""
        times = self.day_portion(times)
        
        imsak = self.sun_angle_time(self.evaluate(self.settings.Imsak), times[IMSAK], 'ccw')
        sunrise = self.sun_angle_time(self.rise_set_angle(), times[SUNRISE], 'ccw')
        fajr = self.sun_angle_time(self.evaluate(self.settings.Fajr), times[FAJR], 'ccw')
        dhuhr = self.mid_day(times[ZHUHR])
        asr = self.asr_time(self.asr_factor(), times[ASR])
        sunset = self.sun_angle_time(self.rise_set_angle(), times[SUNSET])
        maghrib = self.sun_angle_time(self.evaluate(self.settings.Maghrib), times[MAGHRIB])
        isha = self.sun_angle_time(self.evaluate(self.settings.Isha), times[ISHA])
        
        return {
            FAJR: fajr,
            SUNRISE: sunrise,
            ZHUHR: dhuhr,
            ASR: asr,
            SUNSET: sunset,
            MAGHRIB: maghrib,
            ISHA: isha,
            IMSAK: imsak,
        }
    
    def gregorian_to_julian_date(self) -> float:
        """Convert Gregorian date to Julian date."""
        year = self.date.year
        month = self.date.month
        day = self.date.day
        
        if month <= 2:
            year -= 1
            month += 12
        
        a = year // 100
        b = 2 - a + (a // 4)
        
        jd = (365.25 * (year + 4716) + 30.6001 * (month + 1) + day + b - 1524.5)
        
        # Add fraction of day
        dayfrac = self.date.hour / 24 - 0.5
        if dayfrac < 0:
            dayfrac += 1
        
        frac = dayfrac + (self.date.minute + self.date.second / 60) / 60 / 24
        
        return jd + frac
    
    def asr_time(self, factor: float, time: float) -> float:
        """Calculate Asr prayer time."""
        julian_date = self.gregorian_to_julian_date()
        decl = self.sun_position(julian_date + time)['declination']
        
        angle = -DMath.arccot(factor + DMath.tan(abs(self.latitude - decl)))
        
        return self.sun_angle_time(angle, time)
    
    def sun_angle_time(self, angle: float, time: float, direction: Optional[str] = None) -> float:
        """Calculate time when sun is at a specific angle."""
        julian_date = (self.julian_date(self.date.year, self.date.month, self.date.day) - 
                      self.longitude / (15 * 24))
        decl = self.sun_position(julian_date + time)['declination']
        noon = self.mid_day(time)
        
        p1 = -DMath.sin(angle) - DMath.sin(decl) * DMath.sin(self.latitude)
        p2 = DMath.cos(decl) * DMath.cos(self.latitude)
        cos_range = p1 / p2
        
        cos_range = max(-1, min(1, cos_range))  # Clamp to [-1, 1]
        
        t = 1/15 * DMath.arccos(cos_range)
        
        if direction == 'ccw':
            return noon - t
        else:
            return noon + t
    
    def asr_factor(self) -> float:
        """Get the Asr shadow factor."""
        if self.asr_shadow_factor is not None:
            return self.asr_shadow_factor
        
        if self.school == SCHOOL_STANDARD:
            return 1
        elif self.school == SCHOOL_HANAFI:
            return 2
        else:
            return 0
    
    def rise_set_angle(self) -> float:
        """Calculate rise/set angle."""
        angle = 0.0347 * math.sqrt(self.elevation)  # an approximation
        return 0.833 + angle
    
    def sun_position(self, julian_date: float) -> Dict[str, float]:
        """Calculate sun position (declination and equation of time)."""
        # compute declination angle of sun and equation of time
        # Ref: http://aa.usno.navy.mil/faq/docs/SunApprox.php
        d = julian_date - 2451545.0
        g = DMath.fix_angle(357.529 + 0.98560028 * d)
        q = DMath.fix_angle(280.459 + 0.98564736 * d)
        l = DMath.fix_angle(q + 1.915 * DMath.sin(g) + 0.020 * DMath.sin(2 * g))
        
        r = 1.00014 - 0.01671 * DMath.cos(g) - 0.00014 * DMath.cos(2 * g)
        e = 23.439 - 0.00000036 * d
        
        ra = DMath.arctan2(DMath.cos(e) * DMath.sin(l), DMath.cos(l)) / 15
        eqt = q / 15 - DMath.fix_hour(ra)
        decl = DMath.arcsin(DMath.sin(e) * DMath.sin(l))
        
        return {
            'declination': decl,
            'equation': eqt
        }
    
    def julian_date(self, year: int, month: int, day: int) -> float:
        """Convert date to Julian date."""
        if month <= 2:
            year -= 1
            month += 12
        
        a = year // 100
        b = 2 - a + (a // 4)
        
        jd = (365.25 * (year + 4716) + 30.6001 * (month + 1) + day + b - 1524.5)
        
        return jd
    
    def mid_day(self, time: float) -> float:
        """Calculate midday time."""
        julian_date = (self.julian_date(self.date.year, self.date.month, self.date.day) - 
                      self.longitude / (15 * 24))
        eqt = self.sun_position(julian_date + time)['equation']
        noon = DMath.fix_hour(12 - eqt)
        
        return noon
    
    def day_portion(self, times: Dict[str, float]) -> Dict[str, float]:
        """Convert hours to day portions."""
        return {prayer: time / 24 for prayer, time in times.items()}
    
    def set_method(self, method: str = Method.METHOD_MWL):
        """Set the calculation method."""
        if method in self.method_codes:
            self.method = method
        else:
            self.method = Method.METHOD_MWL  # Default to MWL
    
    def set_asr_juristic_method(self, method: str = SCHOOL_STANDARD):
        """Set the Asr juristic method."""
        if method in [SCHOOL_HANAFI, SCHOOL_STANDARD]:
            self.school = method
        else:
            self.school = SCHOOL_STANDARD
    
    def set_school(self, school: str = SCHOOL_STANDARD):
        """Set the school (same as set_asr_juristic_method)."""
        self.set_asr_juristic_method(school)
    
    def set_midnight_mode(self, mode: str = MIDNIGHT_MODE_STANDARD):
        """Set the midnight mode."""
        if mode in [MIDNIGHT_MODE_JAFARI, MIDNIGHT_MODE_STANDARD]:
            self.midnight_mode = mode
        else:
            self.midnight_mode = MIDNIGHT_MODE_STANDARD
    
    def set_latitude_adjustment_method(self, method: str = LATITUDE_ADJUSTMENT_METHOD_ANGLE):
        """Set the latitude adjustment method."""
        valid_methods = [
            LATITUDE_ADJUSTMENT_METHOD_MOTN,
            LATITUDE_ADJUSTMENT_METHOD_ANGLE,
            LATITUDE_ADJUSTMENT_METHOD_ONESEVENTH,
            LATITUDE_ADJUSTMENT_METHOD_NONE
        ]
        if method in valid_methods:
            self.latitude_adjustment_method = method
        else:
            self.latitude_adjustment_method = LATITUDE_ADJUSTMENT_METHOD_ANGLE
    
    def set_time_format(self, format: str = TIME_FORMAT_24H):
        """Set the time format."""
        valid_formats = [
            TIME_FORMAT_ISO8601,
            TIME_FORMAT_24H,
            TIME_FORMAT_FLOAT,
            TIME_FORMAT_12hNS,
            TIME_FORMAT_12H
        ]
        if format in valid_formats:
            self.time_format = format
        else:
            self.time_format = TIME_FORMAT_24H
    
    def tune(self, imsak: int = 0, fajr: int = 0, sunrise: int = 0, dhuhr: int = 0,
             asr: int = 0, maghrib: int = 0, sunset: int = 0, isha: int = 0, 
             midnight: int = 0):
        """Set time offsets for tuning prayer times."""
        self.offset = {
            IMSAK: imsak,
            FAJR: fajr,
            SUNRISE: sunrise,
            ZHUHR: dhuhr,
            ASR: asr,
            MAGHRIB: maghrib,
            SUNSET: sunset,
            ISHA: isha,
            MIDNIGHT: midnight
        }
    
    def load_methods(self):
        """Load all available calculation methods."""
        self.methods = Method.get_methods()
        self.method_codes = Method.get_method_codes()
    
    def get_methods(self):
        """Get all available methods."""
        return self.methods
    
    def get_method(self):
        """Get the current method."""
        return self.method
    
    def get_meta(self) -> Dict[str, Any]:
        """Get metadata about the current calculation."""
        result = {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timezone': str(self.date.tzinfo) if self.date.tzinfo else 'UTC',
            'method': self.methods[self.method],
            'latitudeAdjustmentMethod': self.latitude_adjustment_method,
            'midnightMode': self.midnight_mode,
            'school': self.school,
            'offset': self.offset,
        }
        
        if 'offset' in result['method']:
            del result['method']['offset']
        
        if self.method == Method.METHOD_MOONSIGHTING:
            result['latitudeAdjustmentMethod'] = LATITUDE_ADJUSTMENT_METHOD_NONE
            result['method']['params']['shafaq'] = self.shafaq
        
        return result 