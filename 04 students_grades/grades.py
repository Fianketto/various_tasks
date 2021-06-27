MIN_GRADE = 2
MAX_GRADE = 12
MIN_HIGH_GRADE = 10


def get_pupil_count():
    while True:
        n = int(input("Введите количество учеников\n"))
        n = int(n)
        if n > 0:
            break
        else:
            print("Количество учеников должно быть больше 0")
    return n


def get_pupil_grades(n):
    get_new_data = True
    grades = [[] for i in range(n)]
    while get_new_data:
        get_new_data = False
        print(f"Введите двумерный массив с оценками учеников. "
              f"В каждой строке введите оценки очередного ученика, разделяя их пробелами")
        for i in range(n):
            grades[i] = list(map(int, input().split()))
        for i in range(n):
            if len(grades[i]) == 0:
                get_new_data = True
            for j in range(len(grades[i])):
                if grades[i][j] < MIN_GRADE or grades[i][j] > MAX_GRADE:
                    get_new_data = True
        if get_new_data:
            print(f"Неверные данные. Убедитесь, что все оценки лежат в диапазоне от {MIN_GRADE} до {MAX_GRADE} "
                  f"и у каждого ученика есть хотя бы одна оценка")
    return grades


def get_average_grades(grades):
    pupil_count = len(grades)
    average_grade = [None for i in range(pupil_count)]
    for i in range(pupil_count):
        s = 0
        grade_count = len(grades[i])
        for j in range(grade_count):
            s += grades[i][j]
        average_grade[i] = round(s / grade_count, 3)

    print("Средние оценки учеников (счет начинается с 1):")
    for i in range(pupil_count):
        print(f"{i + 1}: {average_grade[i]}")

    return average_grade


def get_max_and_min_averages(average_grade):
    max_average_grade = max(average_grade)
    min_average_grade = min(average_grade)
    pupils_max = [i + 1 for i, avg in enumerate(average_grade) if avg == max_average_grade]
    pupils_min = [i + 1 for i, avg in enumerate(average_grade) if avg == min_average_grade]

    print("\nНаибольший средний балл и список номеров учеников с таким баллом:")
    print(f"{max_average_grade}: {pupils_max}")
    print("\nНаименьший средний балл и список номеров учеников с таким баллом:")
    print(f"{min_average_grade}: {pupils_min}")


def get_pupils_with_high_grades(grades):
    pupil_count = len(grades)
    pupils_with_high_grades = []
    for i in range(pupil_count):
        if min(grades[i]) >= MIN_HIGH_GRADE:
            pupils_with_high_grades.append(i + 1)
    if pupils_with_high_grades:
        print(f"\nНомера учеников, у которых оценки только высокого уровня:\n{pupils_with_high_grades}")
    else:
        print("\nНет учеников с оценками только высокого уровня")


def get_two_count(grades):
    pupil_count = len(grades)
    two_count = 0
    for i in range(pupil_count):
        two_count += grades[i].count(2)
    print(f"\nКоличество двоек во всем наборе оценок:\n{two_count}")


if __name__ == "__main__":
    pupil_count = get_pupil_count()
    grades = get_pupil_grades(pupil_count)
    average_grade = get_average_grades(grades)
    get_max_and_min_averages(average_grade)
    get_pupils_with_high_grades(grades)
    get_two_count(grades)

