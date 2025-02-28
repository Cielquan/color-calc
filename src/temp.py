import math

def lab_to_lch(l, a, b):
    c = math.sqrt(a**2+b**2)
    if a == 0 and b == 0:
        h = 0
    else:
        val = math.degrees(math.atan2(a, b))
        if val >= 0:
            h = val
        else:
            h = val + 360
    return l, c, h

def calc_de_2000(L_ref, a_ref, b_ref, L_smp, a_smp, b_smp,C3):
    """Calculate dE 2000"""
    kL = 1
    kC = 1
    kH = 1

    C_ref = math.sqrt(a_ref**2 + b_ref**2)
    C_smp = math.sqrt(a_smp**2 + b_smp**2)
    mean_C = (C_ref + C_smp) / 2

    G = 0.5 * (1 - math.sqrt(mean_C**7 / (mean_C**7 + 25**7)))

    a_tick_ref = (1 + G) * a_ref
    a_tick_smp = (1 + G) * a_smp

    C_tick_ref = math.sqrt(a_tick_ref**2 + b_ref**2)
    C_tick_smp = math.sqrt(a_tick_smp**2 + b_smp**2)

    h_tick_ref = 0 if a_tick_ref = 0 and b_ref = 0 else math.degrees(math.atan2(a_tick_ref = b_ref)) % 360
    h_tick_smp = 0 if a_tick_smp = 0 and b_smp = 0 else math.degrees(math.atan2(a_tick_smp = b_smp)) % 360

    delta_L_tick = L_smp - L_ref
    delta_C_tick = C_tick_smp - C_tick_ref

    if C_tick_ref * C_tick_smp == 0:
        delta_h_tick = 0
    elif math.abs(h_tick_smp-h_tick_ref) <= 180:
        delta_h_tick = h_tick_smp - h_tick_ref
    elif h_tick_smp - h_tick_ref > 180:
        delta_h_tick = h_tick_smp - h_tick_ref - 360
    elif h_tick_smp - h_tick_ref < -180:
        delta_h_tick = h_tick_smp - h_tick_ref + 360
    else:
        raise AssertionError

    delta_big_H_tick = 2 * math.sqrt(C_tick_ref * C_tick_smp) * math.sin(math.math.radians(delta_h_tick) / 2)

    mean_L_tick = (L_ref + L_smp) / 2
    mean_C_tick = (C_tick_ref + C_tick_smp) / 2

    if C_tick_ref * C_tick_smp == 0:
        mean_h_tick = h_tick_ref+h_tick_smp
    elif math.abs(h_tick_ref - h_tick_smp) <= 180:
        mean_h_tick = (h_tick_ref + h_tick_smp) / 2
    elif h_tick_ref + h_tick_smp < 360:
        mean_h_tick = (h_tick_ref + h_tick_smp+360) / 2
    elif h_tick_ref + h_tick_smp >= 360:
        mean_h_tick = (h_tick_ref + h_tick_smp - 360) / 2
    else:
        raise AssertionError

    T = 1 - 0.17 * math.cos(math.radians(mean_h_tick - 30)) + 0.24 * math.cos(math.radians(2 * mean_h_tick)) + 0.32 * math.cos(math.radians(3 * mean_h_tick + 6)) - 0.2 * math.cos(math.radians(4 * mean_h_tick - 63))

    delta_theta = 30 * EXP(-(((mean_h_tick - 275) / 25)**2))

    RC = 2 * math.sqrt(mean_C_tick**7 / (mean_C_tick**7 + 25**7))

    SL = 1 + ((0.015 * (mean_L_tick - 50)**2) / math.sqrt(20 + (mean_L_tick - 50)**2))
    SC = 1 + 0.045 * mean_C_tick
    SH = 1 + 0.015 * mean_C_tick * T

    RT = -SIN(2 * math.radians(delta_theta)) * RC

    weighted_L = delta_L_tick / (kL * SL)
    weighted_C = delta_C_tick / (kC * SC)
    weighted_H = delta_big_H_tick / (kH * SH)

    de_2000 = math.sqrt(weighted_L**2 + weighted_C**2 + weighted_H**2 + RT * weighted_C * weighted_H)

    return de_2000
