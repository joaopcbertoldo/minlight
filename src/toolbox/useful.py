from math import cos, sin, atan2, pi

from numpy.core.umath import sqrt


def solutions_formule_quadratique(a, b, c):
    return (-b - sqrt(b ** 2 - 4 * a * c)) / 2 / a, (-b + sqrt(b ** 2 - 4 * a * c)) / 2 / a


def get_plane_normal(surface, verticies, reference_point):
    centre_plane = verticies[surface[0]] + verticies[surface[1]] + verticies[surface[2]] + verticies[surface[3]]
    centre_plane /= 4
    normal = centre_plane - reference_point
    return normal.direction()


def x_sph(latitude_angle, longitude_angle):
    return cos(latitude_angle) * sin(longitude_angle)


def y_sph(latitude_angle, longitude_angle):
    return cos(latitude_angle) * cos(longitude_angle)


def z_sph(latitude_angle):
    return sin(latitude_angle)


def secondes_dans_horaire(heure1):
    return 60 * (int(heure1.split(':')[0])*60 + int(heure1.split(':')[1]))


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