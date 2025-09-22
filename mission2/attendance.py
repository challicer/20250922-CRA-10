import abc
from abc import ABC

class Action(ABC):
    def __init__(self):
        self.attendance_point = 0
        self.weekend_count = 0
        self.wednesday_count = 0

    @abc.abstractmethod
    def add_attendance_point(self, point):
        pass

    @abc.abstractmethod
    def add_wednesday_attendance_count(self, count):
        pass


    @abc.abstractmethod
    def add_weekend_attendance_count(self, count):
        pass

class WednesdayAction(Action):
    def __init__(self):
        super().__init__()
        self.attendance_point = 3
        self.weekend_count = 0
        self.wednesday_count = 1

    def add_attendance_point(self, point):
        return point + self.attendance_point

    def add_wednesday_attendance_count(self, count):
        return count + self.wednesday_count

    def add_weekend_attendance_count(self, count):
        return count + self.weekend_count


class WeekendAction(Action):
    def __init__(self):
        super().__init__()
        self.attendance_point = 2
        self.weekend_count = 1
        self.wednesday_count = 0

    def add_attendance_point(self, point):
        return point + self.attendance_point

    def add_wednesday_attendance_count(self, count):
        return count + self.wednesday_count

    def add_weekend_attendance_count(self, count):
        return count + self.weekend_count


class NormalAction(Action):
    def __init__(self):
        super().__init__()
        self.attendance_point = 1
        self.weekend_count = 0
        self.wednesday_count = 0

    def add_attendance_point(self, point):
        return point + self.attendance_point

    def add_wednesday_attendance_count(self, count):
        return count + self.wednesday_count

    def add_weekend_attendance_count(self, count):
        return count + self.weekend_count


class Grade(ABC):

    @abc.abstractmethod
    def get_grade_str(self):
        pass


class GoldGrade(Grade):
    def get_grade_str(self):
        return "GOLD"


class SilverGrade(Grade):
    def get_grade_str(self):
        return "SILVER"


class NormalGrade(Grade):
    def get_grade_str(self):
        return "NORMAL"


class NormalPlayer():
    def __init__(self, player_name, player_id):
        self.player_name = player_name
        self.player_id = player_id
        self.wednesday_attendance_count = 0
        self.weekend_attendance_count = 0
        self.attendance_point = 0
        self.add_action = NormalAction()
        self.grade_class = NormalGrade()
        self.gold_grade_cut = 50
        self.silver_grade_cut = 30
        self.BONUS_MIN_DAYS = 10
        self.BONUS_POINT = 10

    def set_action(self, weekday):
        if (weekday == "wednesday"):
            self.add_action = WednesdayAction()
        elif (weekday in ["saturday", "sunday"]):
            self.add_action = WeekendAction()
        else:
            self.add_action = NormalAction()

    def set_grade(self):
        if self.attendance_point >= self.gold_grade_cut:
            self.grade_class = GoldGrade()
        elif self.attendance_point >= self.silver_grade_cut:
            self.grade_class = SilverGrade()
        else:
            self.grade_class = NormalGrade()

    def get_grade(self):
        return self.grade_class.get_grade_str()

    def attendance_action(self, weekday):
        self.set_action(weekday)
        self.attendance_point = self.add_action.add_attendance_point(self.attendance_point)
        self.weekend_attendance_count = self.add_action.add_weekend_attendance_count(self.weekend_attendance_count)
        self.wednesday_attendance_count = self.add_action.add_wednesday_attendance_count(self.wednesday_attendance_count)

    def get_bonus_score(self):
        if self.wednesday_attendance_count >= self.BONUS_MIN_DAYS:
            self.attendance_point += self.BONUS_POINT
        if self.weekend_attendance_count >= self.BONUS_MIN_DAYS:
            self.attendance_point += self.BONUS_POINT

    def check_removed_player(self):
        if (self.grade_class.get_grade_str() == "NORMAL"
                and self.wednesday_attendance_count == 0
                and self.weekend_attendance_count == 0):
            return self.player_name
        else:
            return ""


class AttendanceManager():
    def __init__(self):
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
        if player_name not in self.player_attendance.keys():
            self.init_player(player_name)
        self.player_attendance[player_name].attendance_action(attendance_weekday)

    def init_player(self, player_name):
        self.player_attendance[player_name] = NormalPlayer(player_name, self.get_player_id())


    def check_bonus_day_count(self):
        for player_name in self.player_attendance.keys():
            self.player_attendance[player_name].get_bonus_score()

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
            check_removed = self.player_attendance[player_name].check_removed_player()
            if check_removed != "":
                print(player_name)

    def grade_player(self):
        for player_name in self.player_attendance.keys():
            self.player_attendance[player_name].set_grade()
            print(
                f"NAME : {player_name}, POINT : {self.player_attendance[player_name].attendance_point}, GRADE : {self.player_attendance[player_name].get_grade()}")

if __name__ == "__main__":
    test_env = AttendanceManager()
    test_env.run_attendance_check("./attendance_weekday_500.txt")
