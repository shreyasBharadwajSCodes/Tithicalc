from __future__ import division
from math import ceil
from collections import namedtuple as struct
import swisseph as swe


Date = struct('Date', ['year', 'month', 'day'])
Place = struct('Place', ['latitude', 'longitude', 'timezone'])
place_details = Place(21.1458, 79.0882, +5.5)

_rise_flags = swe.BIT_DISC_CENTER + swe.BIT_NO_REFRACTION

set_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_LAHIRI)
reset_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)

gregorian_to_jd = lambda date: swe.julday(date.year, date.month, date.day, 0.0)
jd_to_gregorian = lambda jd: swe.revjul(jd, swe.GREG_CAL)

def inverse_lagrange(x, y, ya):
    assert(len(x) == len(y))
    total = 0
    for i in range(len(x)):
        numer = 1
        denom = 1
        for j in range(len(x)):
            if j != i:
                numer *= (ya - y[j])
                denom *= (y[i] - y[j])
        total += numer * x[i] / denom

    return total

def to_dms(deg):
    d, m, s = to_dms_prec(deg)
    return [d, m, int(s)]

def unwrap_angles(angles):
    result = angles
    for i in range(1, len(angles)):
        if result[i] < result[i-1]: result[i] += 360
    assert(result == sorted(result))
    return result

def to_dms_prec(deg):
    d = int(deg)
    mins = (deg - d) * 60
    m = int(mins)
    s = round((mins - m) * 60, 6)
    return [d, m, s]

def sidereal_longitude(jd, planet):
    set_ayanamsa_mode()
    longi = swe.calc_ut(jd, planet, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
    reset_ayanamsa_mode()
    return longi[0][0] % 360

solar_longitude = lambda jd: sidereal_longitude(jd, swe.SUN)
lunar_longitude = lambda jd: sidereal_longitude(jd, swe.MOON)

def lunar_phase(jd):
    solar_long = solar_longitude(jd)
    lunar_long = lunar_longitude(jd)
    moon_phase = (lunar_long - solar_long) % 360
    return moon_phase

def sunrise(jd, place):
    lat, lon, tz = place
    geop = (lon,lat,0)
    result = swe.rise_trans(jd - tz/24, swe.SUN,_rise_flags + swe.CALC_RISE,geop)
    rise = result[1][0]
    return [rise + tz/24., to_dms((rise - jd) * 24 + tz)]

def tithi(jd, place):
    tz = place.timezone
    rise = sunrise(jd, place)[0] - tz / 24
    moon_phase = lunar_phase(rise)
    today = ceil(moon_phase / 12)
    degrees_left = today * 12 - moon_phase
    offsets = [0.25, 0.5, 0.75, 1.0]
    lunar_long_diff = [ (lunar_longitude(rise + t) - lunar_longitude(rise)) % 360 for t in offsets ]
    solar_long_diff = [ (solar_longitude(rise + t) - solar_longitude(rise)) % 360 for t in offsets ]
    relative_motion = [ moon - sun for (moon, sun) in zip(lunar_long_diff, solar_long_diff) ]
    y = relative_motion
    x = offsets
    approx_end = inverse_lagrange(x, y, degrees_left)
    ends = (rise + approx_end -jd) * 24 + tz
    answer = [int(today), to_dms(ends)]
    moon_phase_tmrw = lunar_phase(rise + 1)
    tomorrow = ceil(moon_phase_tmrw / 12)
    isSkipped = (tomorrow - today) % 30 > 1
    if isSkipped:
        leap_tithi = today + 1
        degrees_left = leap_tithi * 12 - moon_phase
        approx_end = inverse_lagrange(x, y, degrees_left)
        ends = (rise + approx_end -jd) * 24 + place.timezone
        leap_tithi = 1 if today == 30 else leap_tithi
        answer += [int(leap_tithi), to_dms(ends)]
    return answer

def vaar(jd):
  """Weekday for given Julian day. 0 = Sunday, 1 = Monday,..., 6 = Saturday"""
  return int(ceil(jd + 1) % 7)
'''
Tests below
#Date format is in yyyy / mm / dd
Tithi gives the tithi value and end time
Tithi -> 1 => Shukla Paksha
15 -> onwards it is krishna paksha
'''

if __name__ == '__main__':
    date1 = gregorian_to_jd(Date(2023, 1, 8))
    print(tithi(date1,place_details))