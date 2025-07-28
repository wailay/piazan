"""
Mathematical utility functions for prayer times calculations.
"""

import math


class DMath:
    """Mathematical utility class for prayer times calculations."""
    
    @staticmethod
    def dtr(d):
        """Convert degrees to radians."""
        return (d * math.pi) / 180.0
    
    @staticmethod
    def rtd(r):
        """Convert radians to degrees."""
        return (r * 180.0) / math.pi
    
    @staticmethod
    def sin(d):
        """Sine function with degrees input."""
        return math.sin(DMath.dtr(d))
    
    @staticmethod
    def cos(d):
        """Cosine function with degrees input."""
        return math.cos(DMath.dtr(d))
    
    @staticmethod
    def tan(d):
        """Tangent function with degrees input."""
        return math.tan(DMath.dtr(d))
    
    @staticmethod
    def arcsin(d):
        """Arcsine function returning degrees."""
        return DMath.rtd(math.asin(d))
    
    @staticmethod
    def arccos(d):
        """Arccosine function returning degrees."""
        return DMath.rtd(math.acos(d))
    
    @staticmethod
    def arctan(d):
        """Arctangent function returning degrees."""
        return DMath.rtd(math.atan(d))
    
    @staticmethod
    def arccot(x):
        """Arccotangent function returning degrees."""
        return DMath.rtd(math.atan(1/x))
    
    @staticmethod
    def arctan2(y, x):
        """Arctangent2 function returning degrees."""
        return DMath.rtd(math.atan2(y, x))
    
    @staticmethod
    def fix_angle(a):
        """Fix angle to 0-360 range."""
        return DMath.fix(a, 360)
    
    @staticmethod
    def fix_hour(a):
        """Fix hour to 0-24 range."""
        return DMath.fix(a, 24)
    
    @staticmethod
    def fix(a, b):
        """Fix a value to 0-b range."""
        a = a - b * (a // b)
        return a + b if a < 0 else a 