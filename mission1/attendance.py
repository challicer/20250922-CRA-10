user_attendance_data = {}
id_cnt = 0

points = [0] * 100
grade = [0] * 100
names = [''] * 100
wed = [0] * 100
weeken = [0] * 100

def input2(user_name, weekday):
    global id_cnt

    if user_name not in user_attendance_data:
        id_cnt += 1
        user_attendance_data[user_name] = id_cnt
        names[id_cnt] = user_name

    id2 = user_attendance_data[user_name]

    add_point = 0
    WEEKEND = ["saturday", "sunday"]

    if weekday in WEEKEND:
        add_point += 2
        weeken[id2] += 1
    if weekday == "monday":
        add_point += 1
    elif weekday == "tuesday":
        add_point += 1
    elif weekday == "wednesday":
        add_point += 3
        wed[id2] += 1
    elif weekday == "thursday":
        add_point += 1
    elif weekday == "friday":
        add_point += 1
    points[id2] += add_point


def read_raw_text(file_name:str):
    try:
        with open(file_name, encoding='utf-8') as f:
            lines = f.readlines()
            return [line.strip().split() for line in lines]
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

def run_attendance_check(file_name:str):
    user_attendance_raw_data = read_raw_text(file_name)
    for user_data in user_attendance_raw_data:
        if len(user_data) != 2:
            continue
        [user_name, weekday] = user_data
        input2(user_name, weekday)

    for i in range(1, id_cnt + 1):
        if wed[i] > 9:
            points[i] += 10
        if weeken[i] > 9:
            points[i] += 10

        if points[i] >= 50:
            grade[i] = 1
        elif points[i] >= 30:
            grade[i] = 2
        else:
            grade[i] = 0

        print(f"NAME : {names[i]}, POINT : {points[i]}, GRADE : ", end="")
        if grade[i] == 1:
            print("GOLD")
        elif grade[i] == 2:
            print("SILVER")
        else:
            print("NORMAL")

    print("\nRemoved player")
    print("==============")
    for i in range(1, id_cnt + 1):
        if grade[i] not in (1, 2) and wed[i] == 0 and weeken[i] == 0:
            print(names[i])


if __name__ == "__main__":
    run_attendance_check("attendance_weekday_500.txt")