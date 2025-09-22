player_name_id_map = {}
points = {}
grade = {}
wednesday_count = {}
weekend_count = {}


def record_player_attendance(player_name: str, weekday: str):
    NORMAL_POINT = 1
    WEEKEND_POINT = 2
    WEDNESDAY_POINT = 3
    WEEKEND = ["saturday", "sunday"]

    if player_name not in player_name_id_map:
        init_player(player_name)

    if weekday in WEEKEND:
        points[player_name] += WEEKEND_POINT
        weekend_count[player_name] += 1
    elif weekday == "wednesday":
        points[player_name] += WEDNESDAY_POINT
        wednesday_count[player_name] += 1
    else:
        points[player_name] += NORMAL_POINT


def init_player(player_name):
    player_name_id_map[player_name] = get_next_id()
    points[player_name] = 0
    grade[player_name] = 0
    wednesday_count[player_name] = 0
    weekend_count[player_name] = 0


def get_next_id():
    if len(player_name_id_map):
        max_id = max([player_id for player_id in player_name_id_map.values()]) + 1
    else:
        max_id = 0
    return max_id


def read_text_file(file_name: str):
    try:
        with open(file_name, encoding='utf-8') as f:
            lines = f.readlines()
            return [line.strip().split() for line in lines]
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


def run_attendance_check(file_name: str):
    user_attendance_raw_data = read_text_file(file_name)
    for user_data in user_attendance_raw_data:
        if len(user_data) != 2:
            continue
        [player_name, weekday] = user_data
        record_player_attendance(player_name, weekday)

    check_bonus_day_count()
    grade_player()
    check_removed_player()


def check_removed_player():
    print("\nRemoved player")
    print("==============")
    for player_name in player_name_id_map.keys():
        if wednesday_count[player_name] == 0 and weekend_count[player_name] == 0:
            print(player_name)


def grade_player():
    GOLD_GRADE_POINT_CUT = 50
    SILVER_GRADE_POINT_CUT = 30
    for user_name in player_name_id_map.keys():
        if points[user_name] >= GOLD_GRADE_POINT_CUT:
            grade[user_name] = "GOLD"
        elif points[user_name] >= SILVER_GRADE_POINT_CUT:
            grade[user_name] = "SILVER"
        else:
            grade[user_name] = "NORMAL"

        print(f"NAME : {user_name}, POINT : {points[user_name]}, GRADE : {grade[user_name]}")


def check_bonus_day_count():
    BONUS_MIN_DAYS = 10
    BONUS_POINT = 10
    for player_name in player_name_id_map.keys():
        if wednesday_count[player_name] >= BONUS_MIN_DAYS:
            points[player_name] += BONUS_POINT
        if weekend_count[player_name] >= BONUS_MIN_DAYS:
            points[player_name] += BONUS_POINT


if __name__ == "__main__":
    run_attendance_check("attendance_weekday_500.txt")