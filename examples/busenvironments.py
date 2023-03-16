"""Various types of bus environments."""

import sys
import os

filepath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(filepath))

from scenario.environment import Environment

########################################################################################################################

citaro_g_3_door = Environment()
citaro_g_3_door.set_dimensions(18, 2.5)

citaro_g_3_door.seat_dimensions = (0.40, 0.40)
citaro_g_3_door.seat_distance = 0.4

citaro_g_3_door.seat_column(0.5, 0.3, 3)
citaro_g_3_door.seat_column(3.15, 0.3, 2, rotation=180)
citaro_g_3_door.seat_column(3.15, 1.8, 2, rotation=180)
citaro_g_3_door.seat_column(3.65, 0.3, 2)
citaro_g_3_door.seat_column(3.65, 1.8, 2)
citaro_g_3_door.seat_row(1.4, 1.8, 2)
citaro_g_3_door.seat_row(1.4, 2.2, 2)
citaro_g_3_door.seat_row(1.4, 0.3, 2)
citaro_g_3_door.seat_row(1.4, 0.7, 2)

citaro_g_3_door.seat_row(4.6, 1.8, 3)
citaro_g_3_door.seat_row(4.6, 2.2, 3)
citaro_g_3_door.seat(6, 0.3, rotation=90)

citaro_g_3_door.seat_column(9.15, 0.3, 2, rotation=180)
citaro_g_3_door.seat_column(9.15, 1.8, 2, rotation=180)

citaro_g_3_door.seat_column(9.65, 0.3, 2)
citaro_g_3_door.seat_column(9.65, 1.8, 2)
citaro_g_3_door.seat_row(13, 2.2, 2)
citaro_g_3_door.seat_row(12.2, 0.3, 3)
citaro_g_3_door.seat_row(12.2, 0.7, 3)

citaro_g_3_door.seat(14.8, 2.1, rotation=180, size=(0.4, 0.6))
citaro_g_3_door.seat(14.8, 0.4, rotation=180, size=(0.4, 0.6))

citaro_g_3_door.seat(15.6, 2.1, size=(0.4, 0.6))
citaro_g_3_door.seat(15.6, 0.4, size=(0.4, 0.6))
citaro_g_3_door.obstacle_object((6.8, 2.5), (6.85, 2), (8.45, 2), (8.5, 2.5), hatch='||')
citaro_g_3_door.obstacle_object((6.8, 0), (6.85, 0.5), (8.45, 0.5), (8.5, 0), hatch='||')
citaro_g_3_door.obstacle_object((16.3, 2.5), (16.3, 2), (17, 1.5), (18, 1.5), linewidth=2, closed=False, fc='none')

citaro_g_3_door.obstacle_polyline((0.7, 0.9), (0.7, 1.6), (6.6, 1.6), (6.6, 2), (8.7, 2), (8.7, 1.6), (10.05, 1.6),
                                  (10.05, 2.5), (12.8, 2.5), (12.8, 2), (14.6, 2), (14.6, 1.8), (16.6, 1.8), (17, 1.5),
                                  (18, 1.5), (18, 0), (16.35, 0), (16.35, 0.7), (14.4, 0.7), (14.4, 0.9), (11.65, 0.9),
                                  (11.65, 0), (10.35, 0), (10.35, 0.9), (8.7, 0.9), (8.7, 0.5), (6.6, 0.5), (6.6, 0.7),
                                  (5.65, 0.7), (5.65, 0), (4.35, 0), (4.35, 0.9), (0.7, 0.9), standing=True)

citaro_g_3_door.obstacle_line((0, 1.6), (1.1, 1.6))
citaro_g_3_door.standing_spot((2, 1.25), (5, 1.25), (8, 1.25), (11, 1.25), (17, 1.25))
citaro_g_3_door.door(5)
citaro_g_3_door.door(11)
citaro_g_3_door.door(17)


########################################################################################################################

citaro_ngt_2_door = Environment()
citaro_ngt_2_door.set_dimensions(12, 2.5)

citaro_ngt_2_door.seat_dimensions = (0.40, 0.40)
citaro_ngt_2_door.seat_distance = 0.4

citaro_ngt_2_door.seat_column(0.5, 0.3, 3)
citaro_ngt_2_door.seat_column(2, 1.8, 2)

citaro_ngt_2_door.seat_row(1.3, 0.7, 2)
citaro_ngt_2_door.seat_row(1.3, 0.3, 2)
citaro_ngt_2_door.seat_column(3.15, 0.3, 2, rotation=180)
citaro_ngt_2_door.seat_column(3.65, 0.3, 2)
citaro_ngt_2_door.seat_column(3.15, 1.8, 2, rotation=180)
citaro_ngt_2_door.seat_column(3.65, 1.8, 2)

citaro_ngt_2_door.seat_row(6.1, 0.3, 3)
citaro_ngt_2_door.seat_row(6.1, 0.7, 3)
citaro_ngt_2_door.seat_row(6.9, 2.2, 2)

citaro_ngt_2_door.seat(8.6, 2.1, rotation=180, size=(0.4, 0.6))
citaro_ngt_2_door.seat(8.6, 0.4, rotation=180, size=(0.4, 0.6))
citaro_ngt_2_door.seat(9.6, 2.1, size=(0.4, 0.6))
citaro_ngt_2_door.seat(9.6, 0.4, size=(0.4, 0.6))

citaro_ngt_2_door.obstacle_object((10.3, 2.5), (10.3, 2), (11, 1.5), (12, 1.5), linewidth=2, closed=False, fc='none')

citaro_ngt_2_door.obstacle_polyline((0.7, 0.9), (0.7, 1.6), (4.05, 1.6), (4.05, 2.5), (6.7, 2.5), (6.7, 2), (8.2, 2),
                                    (8.2, 1.8), (10.6, 1.8), (11, 1.5), (12, 1.5), (12, 0), (10.25, 0), (10.25, 0.7),
                                    (8.1, 0.7), (8.1, 0.9), (5.65, 0.9), (5.65, 0), (4.35, 0), (4.35, 0.9), (0.7, 0.9),
                                    standing=True)

citaro_ngt_2_door.obstacle_line((0, 1.6), (1.8, 1.6))
citaro_ngt_2_door.standing_spot((2, 1.25), (5, 1.25), (7.5, 1.25), (10.9, 1.25))

citaro_ngt_2_door.door(5)
citaro_ngt_2_door.door(10.9)


########################################################################################################################

citaro_ngt_3_door = Environment()
citaro_ngt_3_door.set_dimensions(12, 2.5)

citaro_ngt_3_door.seat_dimensions = (0.40, 0.40)
citaro_ngt_3_door.seat_distance = 0.4

citaro_ngt_3_door.seat_column(0.5, 0.3, 3)
citaro_ngt_3_door.seat_column(2, 1.8, 2)

citaro_ngt_3_door.seat_column(3.15, 0.3, 2, rotation=180)
citaro_ngt_3_door.seat_column(3.65, 0.3, 2)
citaro_ngt_3_door.seat_column(4.45, 0.3, 2)
citaro_ngt_3_door.seat_column(3.15, 1.8, 2, rotation=180)
citaro_ngt_3_door.seat_column(3.65, 1.8, 2)
citaro_ngt_3_door.seat_column(4.45, 1.8, 2)

citaro_ngt_3_door.seat_row(6.9, 0.3, 2)
citaro_ngt_3_door.seat_row(6.9, 0.7, 2)
citaro_ngt_3_door.seat(7.7, 2.2)

citaro_ngt_3_door.seat(8.6, 2.1, rotation=180, size=(0.4, 0.6))
citaro_ngt_3_door.seat(8.6, 0.4, rotation=180, size=(0.4, 0.6))
citaro_ngt_3_door.seat(9.6, 2.1, size=(0.4, 0.6))
citaro_ngt_3_door.seat(9.6, 0.4, size=(0.4, 0.6))

citaro_ngt_3_door.obstacle_object((10.3, 2.5), (10.3, 2), (11, 1.5), (12, 1.5), linewidth=2, closed=False, fc='none')

citaro_ngt_3_door.obstacle_polyline((0.7, 0.9), (0.7, 1.6), (4.85, 1.6), (4.85, 2.5), (7.5, 2.5), (7.5, 2), (8.2, 2),
                                    (8.2, 1.8), (10.6, 1.8), (11, 1.5), (12, 1.5), (12, 0), (10.25, 0), (10.25, 0.7),
                                    (8.1, 0.7), (8.1, 0.9), (6.45, 0.9), (6.45, 0), (5.15, 0), (5.15, 0.9), (2.45, 0.9),
                                    (2.45, 0), (1.15, 0), (1.15, 0.9), (0.7, 0.9), standing=True)


# add to the other vehicles too
citaro_ngt_3_door.obstacle_line((0, 1.6), (1.7, 1.6))
citaro_ngt_3_door.standing_spot((2, 1.25), (5, 1.25), (7.5, 1.25), (10.9, 1.25))

citaro_ngt_3_door.door(1.8)
citaro_ngt_3_door.door(5.8)
citaro_ngt_3_door.door(10.9)


########################################################################################################################

citaro_g_4_door = Environment()
citaro_g_4_door.set_dimensions(18, 2.5)

citaro_g_4_door.seat_dimensions = (0.40, 0.40)
citaro_g_4_door.seat_distance = 0.4

citaro_g_4_door.seat_column(0.5, 0.3, 3)
citaro_g_4_door.seat_column(3.15, 0.3, 2, rotation=180)
citaro_g_4_door.seat_column(3.15, 1.8, 2, rotation=180)
citaro_g_4_door.seat_column(3.65, 0.3, 2)
citaro_g_4_door.seat_column(3.65, 1.8, 2)
citaro_g_4_door.seat_row(1.4, 1.8, 2)
citaro_g_4_door.seat_row(1.4, 2.2, 2)

citaro_g_4_door.seat_row(4.6, 1.8, 3)
citaro_g_4_door.seat_row(4.6, 2.2, 3)
citaro_g_4_door.seat(6, 0.3, rotation=90)

citaro_g_4_door.seat_column(9.15, 0.3, 2, rotation=180)
citaro_g_4_door.seat_column(9.15, 1.8, 2, rotation=180)

citaro_g_4_door.seat_column(9.65, 0.3, 2)
citaro_g_4_door.seat_column(9.65, 1.8, 2)
citaro_g_4_door.seat_row(13, 2.2, 2)
citaro_g_4_door.seat_row(12.2, 0.3, 3)
citaro_g_4_door.seat_row(12.2, 0.7, 3)

citaro_g_4_door.seat(14.8, 2.1, rotation=180, size=(0.4, 0.6))
citaro_g_4_door.seat(14.8, 0.4, rotation=180, size=(0.4, 0.6))

citaro_g_4_door.seat(15.6, 2.1, size=(0.4, 0.6))
citaro_g_4_door.seat(15.6, 0.4, size=(0.4, 0.6))
citaro_g_4_door.obstacle_object((6.8, 2.5), (6.85, 2), (8.45, 2), (8.5, 2.5), hatch='||')
citaro_g_4_door.obstacle_object((6.8, 0), (6.85, 0.5), (8.45, 0.5), (8.5, 0), hatch='||')
citaro_g_4_door.obstacle_object((16.3, 2.5), (16.3, 2), (17, 1.5), (18, 1.5), linewidth=2, closed=False, fc='none')

citaro_g_4_door.obstacle_line((0, 1.6), (1.1, 1.6))

citaro_g_4_door.obstacle_polyline((0.7, 0.9), (0.7, 1.6), (6.6, 1.6), (6.6, 2), (8.7, 2), (8.7, 1.6), (10.05, 1.6),
                                  (10.05, 2.5), (12.8, 2.5), (12.8, 2), (14.6, 2), (14.6, 1.8), (16.6, 1.8), (17, 1.5),
                                  (18, 1.5), (18, 0), (16.35, 0), (16.35, 0.7), (14.4, 0.7), (14.4, 0.9), (11.65, 0.9),
                                  (11.65, 0), (10.35, 0), (10.35, 0.9), (8.7, 0.9), (8.7, 0.5), (6.6, 0.5), (6.6, 0.7),
                                  (5.65, 0.7), (5.65, 0), (4.35, 0), (4.35, 0.9), (2.45, 0.9), (2.45, 0), (1.15, 0),
                                  (1.15, 0.9), (0.7, 0.9), standing=True)

citaro_g_4_door.standing_spot((2, 1.25), (5, 1.25), (8, 1.25), (11, 1.25), (17, 1.25))

citaro_g_4_door.door(1.8)
citaro_g_4_door.door(5)
citaro_g_4_door.door(11)
citaro_g_4_door.door(17)


########################################################################################################################
