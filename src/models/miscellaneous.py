from math import cos, sin, atan2, pi


def x_sph(latitude_angle, longitude_angle):
    return cos(latitude_angle) * sin(longitude_angle)


def y_sph(latitude_angle, longitude_angle):
    return cos(latitude_angle) * cos(longitude_angle)


def z_sph(latitude_angle):
    return sin(latitude_angle)


# secondes dans un horaire donné
def secondes_dans_horaire(heure1):
    return 60 * (int(heure1.split(':')[0])*60 + int(heure1.split(':')[1]))


# angle en degrés entre le nord et le point donné (sens horaire)
def point_azimut(x, y, x_error=0.001, y_error=0.001):
    if abs(x) < x_error:
        if y >= 0:
            return 0
        else:
            return 180

    elif abs(y) < y_error:
        if x >= 0:
            return 90
        else:
            return 270

    else:
        if x > 0 and y > 0:
            return atan2(x, y)
        elif x > 0 > y:
            return atan2(-y, x) * 180 / pi + 90
        elif x < 0 and y < 0:
            return atan2(-x, -y) * 180 / pi + 180
        else:
            return atan2(y, -x) * 180 / pi + 270
