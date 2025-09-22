from abc import ABC

player_attendance = {}

class Action(ABC):
    def add_point(self):
        pass

class WednesdayAction(Action):
    def add_point(self):
        return 3



class PlayerABC(ABC):
    def __init__(self, player_name, player_id):
        self.player_name = player_name
        self.player_id = player_id
        self.grade = "NORMAL"
        self.wednesday_attendance_count = 0
        self.weekend_attendance_count = 0
        self.attendance_point = 0

    def get_grade(self):
        pass

class GoldPlayer(PlayerABC):
    def get_grade(self):
        return "GOLD"

class SilverPlayer(PlayerABC):
    def get_grade(self):
        return "SILVER"


class NormalPlayer(PlayerABC):
    def get_grade(self):
        return "Normal"


class AttendanceManager():
    def __init__(self):
        self.player_name_id_map = {}
        self.attendance_points = {}
        self.player_grade = {}
        self.wednesday_attendance_count = {}
        self.weekend_attendance_count = {}
        self.player_attendance = {}

    def run_attendance_check(self, file_name: str):
        players_attendance_raw_data = self.read_text_file(file_name)
        for player_attendance_data in players_attendance_raw_data:
            if len(player_attendance_data) != 2:
                continue
            [player_name, attendance_weekday] = player_attendance_data
            self.record_player_attendance(player_name, attendance_weekday)

        self.check_bonus_day_count()
        self.grade_player()
        self.check_removed_player()


    def read_text_file(self, file_name: str) -> [str]:
        try:
            with open(file_name, encoding='utf-8') as f:
                lines = f.readlines()
                return [line.strip().split() for line in lines]
        except FileNotFoundError:
            raise FileNotFoundError("파일을 찾을 수 없습니다.")

    def record_player_attendance(self, player_name: str, attendance_weekday: str):
        NORMAL_POINT = 1
        WEEKEND_POINT = 2
        WEDNESDAY_POINT = 3
        WEEKEND = ["saturday", "sunday"]

        if player_name not in self.player_attendance.keys():
            self.init_player(player_name)

        if attendance_weekday in WEEKEND:
            self.player_attendance[player_name].attendance_point += WEEKEND_POINT
            self.player_attendance[player_name].weekend_attendance_count += 1
        elif attendance_weekday == "wednesday":
            self.player_attendance[player_name].attendance_point += WEDNESDAY_POINT
            self.player_attendance[player_name].wednesday_attendance_count += 1
        else:
            self.player_attendance[player_name].attendance_point += NORMAL_POINT

    def init_player(self, player_name):
        self.player_attendance[player_name] = NormalPlayer(player_name, self.get_player_id())


    def check_bonus_day_count(self):
        BONUS_MIN_DAYS = 10
        BONUS_POINT = 10
        for player_name in self.player_attendance.keys():
            if self.player_attendance[player_name].wednesday_attendance_count >= BONUS_MIN_DAYS:
                self.player_attendance[player_name].attendance_point += BONUS_POINT
            if self.player_attendance[player_name].weekend_attendance_count >= BONUS_MIN_DAYS:
                self.player_attendance[player_name].attendance_point += BONUS_POINT

    def get_player_id(self) -> int:
        if len(self.player_attendance.keys()):
            next_id = max([player.player_id for player in self.player_attendance.values()]) + 1
        else:
            next_id = 0
        return next_id

    def check_removed_player(self):
        print("\nRemoved player")
        print("==============")
        for player_name in self.player_attendance.keys():
            if (self.player_attendance[player_name].grade == "NORMAL"
                    and self.player_attendance[player_name].wednesday_attendance_count == 0
                    and self.player_attendance[player_name].weekend_attendance_count == 0):
                print(player_name)

    def grade_player(self):
        GOLD_GRADE_POINT_CUT = 50
        SILVER_GRADE_POINT_CUT = 30
        for player_name in self.player_attendance.keys():
            if self.player_attendance[player_name].attendance_point >= GOLD_GRADE_POINT_CUT:
                self.player_attendance[player_name].grade = "GOLD"
            elif self.player_attendance[player_name].attendance_point >= SILVER_GRADE_POINT_CUT:
                self.player_attendance[player_name].grade = "SILVER"
            else:
                self.player_attendance[player_name].grade = "NORMAL"
            print(
                f"NAME : {player_name}, POINT : {self.player_attendance[player_name].attendance_point}, GRADE : {self.player_attendance[player_name].grade}")

if __name__ == "__main__":
    test_env = AttendanceManager()
    test_env.run_attendance_check("attendance_weekday_500.txt")
