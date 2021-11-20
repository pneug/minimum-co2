# from https://levelup.gitconnected.com/is-your-roof-aimed-well-for-solar-panel-power-8ff21bd97681

import sunpos as sp
from datetime import datetime, timedelta
import math


def main():  # Location of the roof
    latitude = 40.602778
    longitude = -104.741667
    location = (latitude, longitude)  # Roof azimuth
    roof_az = 135  # roof pitch (inches rise per foot horizontal)
    roof_pitch = 5  # Convert roof pitch to elevation angle in degrees
    roof_el = round(90.0 - math.degrees(math.atan(roof_pitch / 12)), 1)  # Get the ideal roof elevation angle when facing south
    best_el = best_roof_elevation(latitude)  # Convert ideal elevation to approximate pitch
    best_pitch = round(12 / math.tan(math.radians(best_el)), 1)  # We can ignore Daylight Savings Time changes
    timezone = -7  # Start time is on a January 1
    the_year = 2022
    tm = datetime(the_year, 1, 1)  # Set the time interval
    delta = timedelta(minutes=10)  # Initialize the solar power factors
    pow_roof, pow_best = 0, 0  # Process relative solar energy for entire year
    while tm.year == the_year:  # Get sun position for this moment
        when = [tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second, timezone]
        sun_az, sun_el = sp.sunpos(when, location, True)  # Is the sun up?
        if sun_el > 0:  # Get angle between roof normal and the Sun
            roof_sun_angle = angle_between(roof_az, roof_el, sun_az, sun_el)  # Get angle between best roof angle and the Sun
            best_sun_angle = angle_between(180, best_el, sun_az, sun_el)  # Get solar energy factor for the roof and for ideal roof
            sol_roof = solar_factor(sun_el, roof_sun_angle)
            sol_best = solar_factor(sun_el, best_sun_angle)  # Tally relative solar power factors
            if roof_sun_angle < 90:
                pow_roof += sol_roof
            if best_sun_angle < 90:
                pow_best += sol_best  # Add the time interval to the date and time
        tm += delta  # Roof efficiency is percent of roof power to best power
    roof_efficiency = round(100 * pow_roof / pow_best)
    print("\nLatitude: ", location[0])
    print("Roof azimuth: ", roof_az)
    print(f"Roof pitch, elevation:  {roof_pitch}:12  {roof_el}")
    print(f"Ideal pitch, elevation:  {best_pitch}:12  {best_el}")
    print("Percent ideal power: ", roof_efficiency)


def angle_between(az1, el1, az2, el2):
    """ 
    Return angle between two azimuth, elevation directions 
    """
    # Convert first direction to spherical
    theta = math.radians(90 - az1)
    phi = math.radians(90.0 - el1)  # Convert first direction to cartesian
    x1 = math.cos(theta) * math.sin(phi)
    y1 = math.sin(theta) * math.sin(phi)
    z1 = math.cos(phi)  # Convert second direction to spherical
    theta = math.radians(90 - az2)
    phi = math.radians(90.0 - el2)  # Convert second direction to cartesian
    x2 = math.cos(theta) * math.sin(phi)
    y2 = math.sin(theta) * math.sin(phi)
    z2 = math.cos(phi)  # Find angle between in degrees
    num = x1 * x2 + y1 * y2 + z1 * z2
    mag1 = math.sqrt(x1 * x1 + y1 * y1 + z1 * z1)
    mag2 = math.sqrt(x2 * x2 + y2 * y2 + z2 * z2)
    angle = math.degrees(math.acos(num / (mag1 * mag2)))
    return angle


def air_mass(elevation):
    """ Return air mass AM for elevation angle """
    # Linear function if near or below horizon
    if elevation < 1:
        return -10.076 * elevation + 36.387  # Published formulas use angle from the zenith_ang
    zenith_ang = 90.0 - elevation  # Get cos of zenith_ang angle
    zcos = math.cos(math.radians(zenith_ang))  # Calculate air mass
    return 1 / (zcos + 0.50572 * (96.07995 - zenith_ang) ** -1.6364)


def solar_intensity(AM):
    """ Return solar intensity as function of air mass """
    return 1.1 * 1.353 * 0.7 ** (AM ** 0.678)


def solar_factor(elevation_sun, angle_to_sun):
    """Return solar factor given elevation angle of the sun
    and the angle between panel normal and the sun."""
    AM = air_mass(elevation_sun)
    sol = solar_intensity(AM)
    rad = math.radians(angle_to_sun)
    return math.cos(rad) * sol


def best_roof_elevation(latitude):
    """ Return approximate best panel elevation angle for given latitude """
    tilt = -0.004261 * latitude ** 2 + 1.05952 * latitude - 1.66
    return round(90 - tilt, 1)


if __name__ == "__main__":
    main()