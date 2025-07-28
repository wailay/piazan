"""
Prayer calculation methods and their parameters.
"""

from prayer_times.contants import FAJR, ISHA, MAGHRIB, MIDNIGHT

class Method:
    """Prayer calculation methods and their parameters."""
    
    # All methods available for computation
    METHOD_JAFARI = 'JAFARI'
    METHOD_KARACHI = 'KARACHI'
    METHOD_ISNA = 'ISNA'
    METHOD_MWL = 'MWL'
    METHOD_MAKKAH = 'MAKKAH'
    METHOD_EGYPT = 'EGYPT'
    METHOD_TEHRAN = 'TEHRAN'
    METHOD_GULF = 'GULF'
    METHOD_KUWAIT = 'KUWAIT'
    METHOD_QATAR = 'QATAR'
    METHOD_SINGAPORE = 'SINGAPORE'
    METHOD_FRANCE = 'FRANCE'
    METHOD_TURKEY = 'TURKEY'
    METHOD_RUSSIA = 'RUSSIA'
    METHOD_MOONSIGHTING = 'MOONSIGHTING'
    METHOD_DUBAI = 'DUBAI'
    METHOD_JAKIM = 'JAKIM'
    METHOD_TUNISIA = 'TUNISIA'
    METHOD_ALGERIA = 'ALGERIA'
    METHOD_KEMENAG = 'KEMENAG'
    METHOD_MOROCCO = 'MOROCCO'
    METHOD_PORTUGAL = 'PORTUGAL'
    METHOD_JORDAN = 'JORDAN'
    METHOD_CUSTOM = 'CUSTOM'
    
    def __init__(self, name='Custom'):
        """Initialize a custom method."""
        self.name = name
        # Default Params
        self.params = {
            FAJR: 15,
            ISHA: 15
        }
    
    def set_fajr_angle(self, angle):
        """Set the Fajr Angle."""
        self.params[FAJR] = angle
    
    def set_maghrib_angle_or_mins(self, angle_or_mins_after_sunset):
        """Set Maghrib angle or minutes after sunset."""
        self.params[MAGHRIB] = angle_or_mins_after_sunset
    
    def set_isha_angle_or_mins(self, angle_or_mins_after_maghrib):
        """Set Isha angle or mins after Maghrib."""
        self.params[ISHA] = angle_or_mins_after_maghrib
    
    @staticmethod
    def get_method_codes():
        """Get all available method codes."""
        return [
            Method.METHOD_MWL,
            Method.METHOD_ISNA,
            Method.METHOD_EGYPT,
            Method.METHOD_MAKKAH,
            Method.METHOD_KARACHI,
            Method.METHOD_TEHRAN,
            Method.METHOD_JAFARI,
            Method.METHOD_GULF,
            Method.METHOD_KUWAIT,
            Method.METHOD_QATAR,
            Method.METHOD_SINGAPORE,
            Method.METHOD_FRANCE,
            Method.METHOD_TURKEY,
            Method.METHOD_RUSSIA,
            Method.METHOD_MOONSIGHTING,
            Method.METHOD_DUBAI,
            Method.METHOD_JAKIM,
            Method.METHOD_TUNISIA,
            Method.METHOD_ALGERIA,
            Method.METHOD_KEMENAG,
            Method.METHOD_MOROCCO,
            Method.METHOD_PORTUGAL,
            Method.METHOD_JORDAN,
            Method.METHOD_CUSTOM,
        ]
    
    @staticmethod
    def get_methods():
        """Get all available methods with their parameters."""
        return {
            Method.METHOD_MWL: {
                'id': 3,
                'name': 'Muslim World League',
                'params': {
                    FAJR: 18,
                    ISHA: 17
                },
                'location': {
                    'latitude': 51.5194682,
                    'longitude': -0.1360365,
                }
            },
            Method.METHOD_ISNA: {
                'id': 2,
                'name': 'Islamic Society of North America (ISNA)',
                'params': {
                    FAJR: 15,
                    ISHA: 15
                },
                'location': {
                    'latitude': 39.70421229999999,
                    'longitude': -86.39943869999999,
                }
            },
            Method.METHOD_EGYPT: {
                'id': 5,
                'name': 'Egyptian General Authority of Survey',
                'params': {
                    FAJR: 19.5,
                    ISHA: 17.5
                },
                'location': {
                    'latitude': 30.0444196,
                    'longitude': 31.2357116,
                }
            },
            Method.METHOD_MAKKAH: {
                'id': 4,
                'name': 'Umm Al-Qura University, Makkah',
                'params': {
                    FAJR: 18.5,
                    ISHA: '90 min'
                },
                'location': {
                    'latitude': 21.3890824,
                    'longitude': 39.8579118
                }
            },
            Method.METHOD_KARACHI: {
                'id': 1,
                'name': 'University of Islamic Sciences, Karachi',
                'params': {
                    FAJR: 18,
                    ISHA: 18
                },
                'location': {
                    'latitude': 24.8614622,
                    'longitude': 67.0099388
                }
            },
            Method.METHOD_TEHRAN: {
                'id': 7,
                'name': 'Institute of Geophysics, University of Tehran',
                'params': {
                    FAJR: 17.7,
                    ISHA: 14,
                    MAGHRIB: 4.5,
                    MIDNIGHT: Method.METHOD_JAFARI
                },
                'location': {
                    'latitude': 35.6891975,
                    'longitude': 51.3889736
                }
            },
            Method.METHOD_JAFARI: {
                'id': 0,
                'name': 'Shia Ithna-Ashari, Leva Institute, Qum',
                'params': {
                    FAJR: 16,
                    ISHA: 14,
                    MAGHRIB: 4,
                    MIDNIGHT: Method.METHOD_JAFARI
                },
                'location': {
                    'latitude': 34.6415764,
                    'longitude': 50.8746035
                }
            },
            Method.METHOD_GULF: {
                'id': 8,
                'name': 'Gulf Region',
                'params': {
                    FAJR: 19.5,
                    ISHA: '90 min'
                },
                'location': {
                    'latitude': 24.1323638,
                    'longitude': 53.3199527
                }
            },
            Method.METHOD_KUWAIT: {
                'id': 9,
                'name': 'Kuwait',
                'params': {
                    FAJR: 18,
                    ISHA: 17.5
                },
                'location': {
                    'latitude': 29.375859,
                    'longitude': 47.9774052
                }
            },
            Method.METHOD_QATAR: {
                'id': 10,
                'name': 'Qatar',
                'params': {
                FAJR: 18,
                    ISHA: '90 min'
                },
                'location': {
                    'latitude': 25.2854473,
                    'longitude': 51.5310398
                }
            },
            Method.METHOD_SINGAPORE: {
                'id': 11,
                'name': 'Majlis Ugama Islam Singapura, Singapore',
                'params': {
                    FAJR: 20,
                    ISHA: 18
                },
                'location': {
                    'latitude': 1.352083,
                    'longitude': 103.819836
                }
            },
            Method.METHOD_FRANCE: {
                'id': 12,
                'name': 'Union Organization Islamic de France',
                'params': {
                    FAJR: 12,
                    ISHA: 12
                },
                'location': {
                    'latitude': 48.856614,
                    'longitude': 2.3522219
                }
            },
            Method.METHOD_TURKEY: {
                'id': 13,
                'name': 'Diyanet İşleri Başkanlığı, Turkey (experimental)',
                'params': {
                    FAJR: 18,
                    ISHA: 17
                },
                'location': {
                    'latitude': 39.9333635,
                    'longitude': 32.8597419
                }
            },
            Method.METHOD_RUSSIA: {
                'id': 14,
                'name': 'Spiritual Administration of Muslims of Russia',
                'params': {
                    FAJR: 16,
                    ISHA: 15
                },
                'location': {
                    'latitude': 54.73479099999999,
                    'longitude': 55.9578555
                }
            },
            Method.METHOD_MOONSIGHTING: {
                'id': 15,
                'name': 'Moonsighting Committee Worldwide (Moonsighting.com)',
                'params': {
                    'shafaq': 'general'
                }
            },
            Method.METHOD_DUBAI: {
                'id': 16,
                'name': 'Dubai (experimental)',
                'params': {
                    FAJR: 18.2,
                    ISHA: 18.2,
                },
                'location': {
                    'latitude': 25.0762677,
                    'longitude': 55.087404
                }
            },
            Method.METHOD_JAKIM: {
                'id': 17,
                'name': 'Jabatan Kemajuan Islam Malaysia (JAKIM)',
                'params': {
                    FAJR: 20,
                    ISHA: 18,
                },
                'location': {
                    'latitude': 3.139003,
                    'longitude': 101.686855
                }
            },
            Method.METHOD_TUNISIA: {
                'id': 18,
                'name': 'Tunisia',
                'params': {
                    FAJR: 18,
                    ISHA: 18,
                },
                'location': {
                    'latitude': 36.8064948,
                    'longitude': 10.1815316
                }
            },
            Method.METHOD_ALGERIA: {
                'id': 19,
                'name': 'Algeria',
                'params': {
                    FAJR: 18,
                    ISHA: 17,
                },
                'location': {
                    'latitude': 36.753768,
                    'longitude': 3.0587561
                }
            },
            Method.METHOD_KEMENAG: {
                'id': 20,
                'name': 'Kementerian Agama Republik Indonesia',
                'params': {
                    FAJR: 20,
                    ISHA: 18,
                },
                'location': {
                    'latitude': -6.2087634,
                    'longitude': 106.845599
                }
            },
            Method.METHOD_MOROCCO: {
                'id': 21,
                'name': 'Morocco',
                'params': {
                    FAJR: 19,
                    ISHA: 17,
                },
                'location': {
                    'latitude': 33.9715904,
                    'longitude': -6.8498129
                }
            },
            Method.METHOD_PORTUGAL: {
                'id': 22,
                'name': 'Comunidade Islamica de Lisboa',
                'params': {
                FAJR: 18,
                    MAGHRIB: '3 min',
                    ISHA: '77 min',
                },
                'location': {
                    'latitude': 38.7222524,
                    'longitude': -9.1393366
                }
            },
            Method.METHOD_JORDAN: {
                'id': 23,
                'name': 'Ministry of Awqaf, Islamic Affairs and Holy Places, Jordan',
                'params': {
                    FAJR: 18,
                    MAGHRIB: '5 min',
                    ISHA: 18,
                },
                'location': {
                    'latitude': 31.9461222,
                    'longitude': 35.923844
                }
            },
            Method.METHOD_CUSTOM: {
                'id': 99
            },
        } 