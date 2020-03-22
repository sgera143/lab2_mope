# Нехай довірча ймовірність = 0.95

from math import *
from random import *

m = 5

def determinant(matrix):
    return matrix[0][0] * matrix[1][1] * matrix[2][2] + matrix[0][1] * matrix[1][2] * matrix[2][0] + matrix[0][2] * \
           matrix[1][0] * matrix[2][1] - matrix[0][2] * matrix[1][1] * matrix[2][0] - matrix[0][1] * matrix[1][0] * \
           matrix[2][2] - matrix[0][0] * matrix[1][2] * matrix[2][1]

def rkr(m):
    table = {2: 1.71, 6: 2.10, 8: 2.27, 10: 2.41, 12: 2.52, 15: 2.64, 20: 2.78}

    for i in range(len(table.keys())):
        if m == list(table.keys())[i]:
            return list(table.values())[i]
        if m > list(table.keys())[i]:
            smaller_than_mkey = list(table.keys())[i]
            smaller_than_m = list(table.values())[i]
            more_than_mkey = list(table.keys())[i+1]
            more_than_m = list(table.values())[i+1]
            return smaller_than_m + (more_than_m - smaller_than_m) * (m - smaller_than_mkey) / (more_than_mkey - smaller_than_mkey)

variant = 5
y_max = (30 - variant) * 10
y_min = (20 - variant) * 10

def main():
    global m

    response_list_1 = [randint(y_min, y_max) for i in range(m)]
    response_list_2 = [randint(y_min, y_max) for j in range(m)]
    response_list_3 = [randint(y_min, y_max) for k in range(m)]

    average_1 = sum(response_list_1) / len(response_list_1)
    average_2 = sum(response_list_2) / len(response_list_2)
    average_3 = sum(response_list_3) / len(response_list_3)

    dispersion_1 = sum((i - average_1) ** 2 for i in response_list_1) / len(response_list_1)
    dispersion_2 = sum((i - average_2) ** 2 for i in response_list_2) / len(response_list_2)
    dispersion_3 = sum((i - average_3) ** 2 for i in response_list_3) / len(response_list_3)

    major_deviation = sqrt((4 * m - 4) / (m * m - 4 * m))

    f_12 = dispersion_1 / dispersion_2 if dispersion_1 >= dispersion_2 else dispersion_2 / dispersion_1
    f_23 = dispersion_2 / dispersion_3 if dispersion_2 >= dispersion_3 else dispersion_3 / dispersion_2
    f_13 = dispersion_1 / dispersion_3 if dispersion_1 >= dispersion_3 else dispersion_3 / dispersion_1

    t_12 = (m - 2) / m * f_12
    t_23 = (m - 2) / m * f_23
    t_13 = (m - 2) / m * f_13

    r_12 = abs(t_12 - 1) / major_deviation
    r_23 = abs(t_23 - 1) / major_deviation
    r_13 = abs(t_13 - 1) / major_deviation

    r_kr = rkr(m)

    print('\ny_min =', y_min, '\ny_max =', y_max)

    print(f'\nЗначення відгуку в діапазоні [{y_min}-{y_max}]:')
    print(*response_list_1, sep='\t')
    print(*response_list_2, sep='\t')
    print(*response_list_3, sep='\t')

    print('\nСереднє значення відгуку в кожній з точок плану:', '\n' + f'{average_1}', '\n' + f'{average_2}', '\n' + f'{average_3}')
    print('\nДисперсії для кожної точки планування:', '\n' + f'{dispersion_1:.3f}', '\n' + f'{dispersion_2:.3f}', '\n' + f'{dispersion_3:.3f}')
    print('\nОсновне відхилення:', f'{major_deviation:.3f}')

    print('r_12=' + f'{r_12:.3f}', '<' if r_12 < r_kr else '>', 'r_kr=' + f'{r_kr:.3f}')
    print('r_23=' + f'{r_23:.3f}', '<' if r_23 < r_kr else '>', 'r_kr=' + f'{r_kr:.3f}')
    print('r_13=' + f'{r_13:.3f}', '<' if r_13 < r_kr else '>', 'r_kr=' + f'{r_kr:.3f}')

    if r_12 < r_kr and r_23 < r_kr and r_13 < r_kr:
        print('\nОднорідність підтверджується з ймовірністю 0.95')
        normalized_x1_x2 = [[-1, -1], [-1, 1], [1, -1]]
        mx_list = [sum(i) / len(i) for i in list(zip(normalized_x1_x2[0], normalized_x1_x2[1], normalized_x1_x2[2]))]
        my = sum([average_1, average_2, average_3]) / len([average_1, average_2, average_3])
        
        a_1 = sum(i[0] ** 2 for i in normalized_x1_x2) / len(normalized_x1_x2)
        a_2 = sum(i[0] * i[1] for i in normalized_x1_x2) / len(normalized_x1_x2)
        a_3 = sum(i[1] ** 2 for i in normalized_x1_x2) / len(normalized_x1_x2)
        a_11 = sum(normalized_x1_x2[i][0] * [average_1, average_2, average_3][i] for i in range(len(normalized_x1_x2))) / len(normalized_x1_x2)
        a_22 = sum(normalized_x1_x2[i][1] * [average_1, average_2, average_3][i] for i in range(len(normalized_x1_x2))) / len(normalized_x1_x2)
        
        matrix_b = [ [1, mx_list[0], mx_list[1]], [mx_list[0], a_1, a_2], [mx_list[1], a_2, a_3] ]
        matrix_b_1 = [ [my, mx_list[0], mx_list[1]], [a_11, a_1, a_2], [a_22, a_2, a_3] ]
        matrix_b_2 = [ [1, my, mx_list[1]], [mx_list[0], a_11, a_2], [mx_list[1], a_22, a_3] ]
        matrix_b_3 = [ [1, mx_list[0], my], [mx_list[0], a_1, a_11], [mx_list[1], a_2, a_22] ]

        b0 = determinant(matrix_b_1) / determinant(matrix_b)
        b1 = determinant(matrix_b_2) / determinant(matrix_b)
        b2 = determinant(matrix_b_3) / determinant(matrix_b)

        print('\nРозрахунок нормованих коефіцієнтів рівняння регресії:')
        for i in normalized_x1_x2:
            print(f'y = b0 + b1 * x1 + b2 * x2 = {b0:.3f} + {b1:.3f} * {i[0]:2} + {b2:.3f} * {i[1]:2}', f' = {b0 + b1 * i[0] + b2 * i[1]:.3f}')

        x1_min = -30
        x1_max = 20
        x2_min = -25
        x2_max = 10

        x_10 = (x1_max + x1_min) / 2
        x_20 = (x2_max + x2_min) / 2

        delta_x1 = (x1_max - x1_min) / 2
        delta_x2 = (x2_max - x2_min) / 2

        a_0 = b0 - b1 * (x_10 / delta_x1) - b2 * (x_20 / delta_x2)
        a_1 = b1 / delta_x1
        a_2 = b2 / delta_x2

        print('\nЗапишемо натуралізоване рівняння регресії:')
        print(f'y = a0 + a_1 * x1 + a_2 * x2 = {a_0:.3f} + {a_1:.3f} * {x1_min:3} + {a_2:.3f} * {x2_min:3}', f' = {a_0 + a_1 * x1_min + a_2 * x2_min:.3f}')
        print(f'y = a0 + a_1 * x1 + a_2 * x2 = {a_0:.3f} + {a_1:.3f} * {x1_min:3} + {a_2:.3f} * {x2_max:3}', f' = {a_0 + a_1 * x1_min + a_2 * x2_max:.3f}')
        print(f'y = a0 + a_1 * x1 + a_2 * x2 = {a_0:.3f} + {a_1:.3f} * {x1_max:3} + {a_2:.3f} * {x2_min:3}', f' = {a_0 + a_1 * x1_max + a_2 * x2_min:.3f}')
        print()

    else:
        print('\nОднорідність не підтвердилася, підвищуємо m на 1\n')
        m += 1
        main()

main()
