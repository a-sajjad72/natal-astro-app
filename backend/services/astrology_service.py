# backend/services/astrology_service.py

from datetime import datetime, timedelta
from typing import Dict, Tuple

import ephem
import pandas as pd
import swisseph as swe

from backend.routes.locations import get_coordinates
from backend.services.astrology_constants import (
    KARANA_NAMES,
    MONTH_NAMES,
    NAKSHATRA_NAMES,
    SENSITIVE_POINTS,
    TITHI_NAMES,
    YOGA_NAMES,
)

swe.set_sid_mode(swe.SIDM_LAHIRI)


class AstrologyService:
    def __init__(self, birth_data: Dict):
        self.birth_data = birth_data
        self._validate_inputs()

        self.birth_data["datetime"] = datetime.strptime(
            f"{birth_data['date']} {birth_data['time']}", "%Y-%m-%d %H:%M"
        )

    def _validate_inputs(self):
        """Convert and validate input data types"""
        required_keys = ["name", "date", "time", "location", "timezone_offset"]
        if not all(key in self.birth_data for key in required_keys):
            raise ValueError("Missing required birth data parameters")

    def calculate(self) -> Dict:
        """Main calculation workflow"""

        # Calculate Julian Day
        self.jd_utc = self._calculate_julian_day(
            self.birth_data["datetime"], self.birth_data["timezone_offset"]
        )

        self.lagna = self._calculate_lagna()
        sunrise_sunset = self._calculate_sunrise_sunset()
        panchang = self._calculate_panchang()
        planet_positions, planet_speeds = self._calculate_planetary_positions()
        sensitive_points = self._calculate_sensitive_points()
        sahams = self._calculate_sahams(self.lagna, planet_positions)

        return {
            "lagna": self.lagna,
            "sunrise_sunset": sunrise_sunset,
            "panchang": panchang,
            "planet_positions": planet_positions,
            "planet_speeds": planet_speeds,
            "sensitive_points": sensitive_points,
            "sahams": sahams,
        }

    def _calculate_julian_day(self, birth_dt: datetime, tz_offset: float) -> float:
        """Convert local datetime to UTC and calculate Julian Day"""
        utc_time = birth_dt - timedelta(hours=tz_offset)
        return swe.julday(
            utc_time.year,
            utc_time.month,
            utc_time.day,
            utc_time.hour + utc_time.minute / 60.0,
        )

    def _calculate_lagna(self) -> float:
        """Calculate Lagna (Ascendant)"""
        houses, cusps = swe.houses(
            self.jd_utc, self.birth_data["latitude"], self.birth_data["longitude"], b"P"
        )
        lagna_tropical = cusps[0]
        ayanamsha = swe.get_ayanamsa(self.jd_utc)
        return (lagna_tropical - ayanamsha) % 360

    def _calculate_sunrise_sunset(self) -> Dict:
        """Calculate sunrise and sunset times"""
        observer = ephem.Observer()
        observer.lat = str(self.birth_data["latitude"])
        observer.lon = str(self.birth_data["longitude"])
        observer.date = self.birth_data["datetime"].strftime("%Y/%m/%d")
        sunrise_utc = observer.previous_rising(ephem.Sun())
        sunset_utc = observer.next_setting(ephem.Sun())

        return {
            "sunrise": ephem.localtime(sunrise_utc).strftime("%I:%M %p"),
            "sunset": ephem.localtime(sunset_utc).strftime("%I:%M %p"),
        }

    def _calculate_panchang(self) -> Dict:
        """Calculate Panchang elements"""
        weekday = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        moon_long = swe.calc_ut(
            self.jd_utc, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SIDEREAL
        )[0]
        sun_long = swe.calc_ut(self.jd_utc, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[
            0
        ]
        # Each Tithi is 12 degrees apar, Shift Tithi by +1 for correct indexing
        tithi_index = int(((moon_long[0] - sun_long[0]) % 360) / 12) + 1
        return {
            "Lunar Month": MONTH_NAMES[(int(sun_long[0] // 30)) % 12],
            "Paksha": "Shukla" if tithi_index < 15 else "Krishna",
            "Tithi": TITHI_NAMES[tithi_index],
            "Weekday": weekday[int(self.jd_utc + 1) % 7],
            "Moon Nakshatra": NAKSHATRA_NAMES[int(moon_long[0] // 13.3333)],
            "Yoga": YOGA_NAMES[int((moon_long[0] + sun_long[0]) / 13.3333) % 27],
            "Karana": KARANA_NAMES[int((moon_long[0] * 2) % 11)],
        }

    def _calculate_planetary_positions(self) -> Tuple[Dict, Dict]:
        """Calculate planetary positions and speeds"""
        PLANETS = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mars": swe.MARS,
            "Mercury": swe.MERCURY,
            "Jupiter": swe.JUPITER,
            "Venus": swe.VENUS,
            "Saturn": swe.SATURN,
            "Rahu": swe.MEAN_NODE,
            "Ketu": swe.MEAN_NODE,
            "Uranus": swe.URANUS,
            "Neptune": swe.NEPTUNE,
            "Pluto": swe.PLUTO,
        }

        positions = {"Lagna": self.lagna}
        speeds = {}
        for name, planet in PLANETS.items():
            pos = swe.calc_ut(
                self.jd_utc, planet, swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
            )[0]
            positions[name] = pos[0] % 360
            speeds[name] = pos[3]

        # Handle Rahu/Ketu
        positions["Ketu"] = (positions["Rahu"] + 180) % 360
        speeds["Ketu"] = speeds["Rahu"]

        return positions, speeds

    def _calculate_sensitive_points(self) -> Dict:
        """Calculate sensitive points"""
        return {
            name: formula(self.jd_utc) for name, formula in SENSITIVE_POINTS.items()
        }

    def _calculate_sahams(self, ascendant: float, positions: Dict) -> Dict:
        """Calculate Sahams"""
        return {
            "Fortune Saham": (ascendant + positions["Moon"] - positions["Sun"]) % 360,
            "Kingdom Saham": (ascendant + positions["Jupiter"] - positions["Sun"])
            % 360,
            "Wealth Saham": (ascendant + positions["Jupiter"] - positions["Moon"])
            % 360,
            "Victory Saham": (ascendant + positions["Mars"] - positions["Sun"]) % 360,
            "Marriage Saham": (ascendant + positions["Venus"] - positions["Moon"])
            % 360,
            "Children Saham": (ascendant + positions["Jupiter"] - positions["Mars"])
            % 360,
            "Father Saham": (ascendant + positions["Sun"] - positions["Saturn"]) % 360,
            "Mother Saham": (ascendant + positions["Moon"] - positions["Venus"]) % 360,
            "Death Saham": (ascendant + positions["Saturn"] - positions["Moon"]) % 360,
            "Exile Saham": (ascendant + positions["Saturn"] - positions["Rahu"]) % 360,
            "Illness Saham": (ascendant + positions["Saturn"] - positions["Mars"])
            % 360,
            "Enemy Saham": (ascendant + positions["Mars"] - positions["Saturn"]) % 360,
            "Slavery Saham": (ascendant + positions["Saturn"] - positions["Mercury"])
            % 360,
            "Knowledge Saham": (ascendant + positions["Mercury"] - positions["Jupiter"])
            % 360,
            "Livelihood Saham": (ascendant + positions["Saturn"] - positions["Moon"])
            % 360,
            "Brothers Saham": (ascendant + positions["Mars"] - positions["Venus"])
            % 360,
            "Fame Saham": (ascendant + positions["Sun"] - positions["Moon"]) % 360,
            "Purity Saham": (ascendant + positions["Moon"] - positions["Saturn"]) % 360,
            "Spirituality Saham": (ascendant + positions["Ketu"] - positions["Moon"])
            % 360,
            "Courage Saham": (ascendant + positions["Mars"] - positions["Mercury"])
            % 360,
            "Education Saham": (ascendant + positions["Jupiter"] - positions["Mercury"])
            % 360,
            "Strength Saham": (ascendant + positions["Sun"] - positions["Saturn"])
            % 360,
            "Land Saham": (ascendant + positions["Moon"] - positions["Venus"]) % 360,
            "Power Saham": (ascendant + positions["Sun"] - positions["Jupiter"]) % 360,
            "Speech Saham": (ascendant + positions["Mercury"] - positions["Moon"])
            % 360,
            "Intelligence Saham": (
                ascendant + positions["Mercury"] - positions["Jupiter"]
            )
            % 360,
            "Longevity Saham": (ascendant + positions["Saturn"] - positions["Moon"])
            % 360,
            "Destruction Saham": (ascendant + positions["Mars"] - positions["Saturn"])
            % 360,
            "Debts Saham": (ascendant + positions["Saturn"] - positions["Rahu"]) % 360,
            "Success Saham": (ascendant + positions["Jupiter"] - positions["Mars"])
            % 360,
            "Honor Saham": (ascendant + positions["Sun"] - positions["Moon"]) % 360,
            "Truth Saham": (ascendant + positions["Moon"] - positions["Saturn"]) % 360,
            "Karma Saham": (ascendant + positions["Sun"] - positions["Mercury"]) % 360,
            "Mind Saham": (ascendant + positions["Moon"] - positions["Venus"]) % 360,
            "Prosperity Saham": (ascendant + positions["Jupiter"] - positions["Moon"])
            % 360,
            "Determination Saham": (ascendant + positions["Mars"] - positions["Sun"])
            % 360,
        }

    def generate_report(self, results: Dict) -> pd.DataFrame:
        """Generate final report DataFrame"""
        # Your existing CSV generation logic
        # Compile final results
        return pd.DataFrame(
            {
                "Parameter": [
                    "Name",
                    "Date (DD-MM-YYYY)",
                    "Time (HH:MM)",
                    "Location",
                    "Latitude",
                    "Longitude",
                    "Sunrise",
                    "Sunset",
                    *results["panchang"].keys(),
                    "Lagna Degree",
                    *results["planet_positions"].keys(),
                    *results["planet_speeds"].keys(),
                    *results["sensitive_points"].keys(),
                    *results["sahams"].keys(),
                ],
                "Value": [
                    self.birth_data["name"],
                    self.birth_data["datetime"].strftime("%d-%m-%Y"),
                    self.birth_data["datetime"].strftime("%H:%M"),
                    ", ".join(self.birth_data["location"].values()).strip(),
                    self.birth_data["latitude"],
                    self.birth_data["longitude"],
                    results["sunrise_sunset"]["sunrise"],
                    results["sunrise_sunset"]["sunset"],
                    *results["panchang"].values(),
                    f"{results['lagna']:.2f}",
                    *results["planet_positions"].values(),
                    *results["planet_speeds"].values(),
                    *results["sensitive_points"].values(),
                    *results["sahams"].values(),
                ],
            }
        )

    def generate_csv(self):
        results = self.calculate()
        report_df = self.generate_report(results)
        return report_df.to_csv(index=False)
