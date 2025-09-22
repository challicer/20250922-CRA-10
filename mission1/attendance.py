player_name_id_map = {}
attendance_points = {}
player_grade = {}
wednesday_attendance_count = {}
weekend_attendance_count = {}


def run_attendance_check(file_name: str):
    players_attendance_raw_data = read_text_file(file_name)
    for player_attendance_data in players_attendance_raw_data:
        if len(player_attendance_data) != 2:
            continue
        [player_name, attendance_weekday] = player_attendance_data
        record_player_attendance(player_name, attendance_weekday)

    check_bonus_day_count()
    grade_player()
    check_removed_player()


def read_text_file(file_name: str) -> [str]:
    try:
        with open(file_name, encoding='utf-8') as f:
            lines = f.readlines()
            return [line.strip().split() for line in lines]
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


def record_player_attendance(player_name: str, attendance_weekday: str):
    NORMAL_POINT = 1
    WEEKEND_POINT = 2
    WEDNESDAY_POINT = 3
    WEEKEND = ["saturday", "sunday"]

    if player_name not in player_name_id_map:
        init_player(player_name)

    if attendance_weekday in WEEKEND:
        attendance_points[player_name] += WEEKEND_POINT
        weekend_attendance_count[player_name] += 1
    elif attendance_weekday == "wednesday":
        attendance_points[player_name] += WEDNESDAY_POINT
        wednesday_attendance_count[player_name] += 1
    else:
        attendance_points[player_name] += NORMAL_POINT


def init_player(player_name):
    player_name_id_map[player_name] = get_player_id()
    attendance_points[player_name] = 0
    wednesday_attendance_count[player_name] = 0
    weekend_attendance_count[player_name] = 0
    player_grade[player_name] = "NORMAL"


def check_bonus_day_count():
    BONUS_MIN_DAYS = 10
    BONUS_POINT = 10
    for player_name in player_name_id_map.keys():
        if wednesday_attendance_count[player_name] >= BONUS_MIN_DAYS:
            attendance_points[player_name] += BONUS_POINT
        if weekend_attendance_count[player_name] >= BONUS_MIN_DAYS:
            attendance_points[player_name] += BONUS_POINT


def get_player_id() -> int:
    if len(player_name_id_map):
        next_id = max([player_id for player_id in player_name_id_map.values()]) + 1
    else:
        next_id = 0
    return next_id


def check_removed_player():
    print("\nRemoved player")
    print("==============")
    for player_name in player_name_id_map.keys():
        if (player_grade[player_name] == "NORMAL"
                and wednesday_attendance_count[player_name] == 0
                and weekend_attendance_count[player_name] == 0):
            print(player_name)


def grade_player():
    GOLD_GRADE_POINT_CUT = 50
    SILVER_GRADE_POINT_CUT = 30
    for player_name in player_name_id_map.keys():
        if attendance_points[player_name] >= GOLD_GRADE_POINT_CUT:
            player_grade[player_name] = "GOLD"
        elif attendance_points[player_name] >= SILVER_GRADE_POINT_CUT:
            player_grade[player_name] = "SILVER"
        else:
            player_grade[player_name] = "NORMAL"

        print(f"NAME : {player_name}, POINT : {attendance_points[player_name]}, GRADE : {player_grade[player_name]}")


if __name__ == "__main__":
    run_attendance_check("attendance_weekday_500.txt")
