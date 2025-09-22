user_attendance_data = {}
id_cnt = 0

points = {}
grade = {}
names = {}
wed = {}
weeken = {}

def input2(user_name, weekday):
    global id_cnt

    if user_name not in user_attendance_data:
        id_cnt += 1
        user_attendance_data[user_name] = id_cnt
        points[user_name] = 0
        grade[user_name] = 0
        wed[user_name] = 0
        weeken[user_name] = 0

    add_point = 0
    WEEKEND = ["saturday", "sunday"]

    if weekday in WEEKEND:
        add_point += 2
        weeken[user_name] += 1
    elif weekday == "wednesday":
        add_point += 3
        wed[user_name] += 1
    else:
        add_point += 1
    points[user_name] += add_point


def read_raw_text(file_name: str):
    try:
        with open(file_name, encoding='utf-8') as f:
            lines = f.readlines()
            return [line.strip().split() for line in lines]
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

def run_attendance_check(file_name: str):
    user_attendance_raw_data = read_raw_text(file_name)
    for user_data in user_attendance_raw_data:
        if len(user_data) != 2:
            continue
        [user_name, weekday] = user_data
        input2(user_name, weekday)

    for user_name, data in user_attendance_data.items():
        if wed[user_name] > 9:
            points[user_name] += 10
        if weeken[user_name] > 9:
            points[user_name] += 10

    for user_name, data in user_attendance_data.items():
        if points[user_name] >= 50:
            grade[user_name] = 1
        elif points[user_name] >= 30:
            grade[user_name] = 2
        else:
            grade[user_name] = 0

        print(f"NAME : {user_name}, POINT : {points[user_name]}, GRADE : ", end="")
        if grade[user_name] == 1:
            print("GOLD")
        elif grade[user_name] == 2:
            print("SILVER")
        else:
            print("NORMAL")

    print("\nRemoved player")
    print("==============")
    for user_name, data in user_attendance_data.items():
        if grade[user_name] not in (1, 2) and wed[user_name] == 0 and weeken[user_name] == 0:
            print(user_name)


if __name__ == "__main__":
    run_attendance_check("attendance_weekday_500.txt")