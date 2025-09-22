user_attendance_data = {}
id_cnt = 0

# dat[사용자ID][요일]
dat = [[0] * 100 for _ in range(100)]
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
    index = 0

    if weekday == "monday":
        index = 0
        add_point += 1
    elif weekday == "tuesday":
        index = 1
        add_point += 1
    elif weekday == "wednesday":
        index = 2
        add_point += 3
        wed[id2] += 1
    elif weekday == "thursday":
        index = 3
        add_point += 1
    elif weekday == "friday":
        index = 4
        add_point += 1
    elif weekday == "saturday":
        index = 5
        add_point += 2
        weeken[id2] += 1
    elif weekday == "sunday":
        index = 6
        add_point += 2
        weeken[id2] += 1

    dat[id2][index] += 1
    points[id2] += add_point


def read_raw_text(file_name:str):
    try:
        with open(file_name, encoding='utf-8') as f:
            lines = f.readlines()
            return [line.strip().split() for line in lines]
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

def input_file(file_name: str):
    user_attendance_raw_data = read_raw_text(file_name)
    for user_data in user_attendance_raw_data:
        if len(user_data) != 2:
            continue
        input2(user_data[0], user_data[1])

    for i in range(1, id_cnt + 1):
        if dat[i][2] > 9:
            points[i] += 10
        if dat[i][5] + dat[i][6] > 9:
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
    input_file("attendance_weekday_500.txt")