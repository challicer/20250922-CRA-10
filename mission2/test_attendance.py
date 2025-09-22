import pytest
from attendance import AttendanceManager
from unittest.mock import patch

@pytest.fixture
def default_test_env():
    return AttendanceManager()


def test_init_env(default_test_env):
    test_env = default_test_env
    assert test_env.player_attendance == {}


def test_read_text_file(default_test_env):
    test_env = default_test_env
    raw_data = test_env.read_text_file("./attendance_weekday_500.txt")
    assert raw_data[:3] == [['Umar', 'monday'], ['Daisy', 'tuesday'], ['Alice', 'tuesday']]

def test_read_text_file_error(default_test_env):
    test_env = default_test_env
    with pytest.raises(FileNotFoundError):
        test_env.read_text_file("INVALID_PATH")


def test_init_player(default_test_env):
    test_env = default_test_env
    player_name = "Umar"
    test_env.init_player(player_name)
    assert test_env.player_attendance[player_name].attendance_point == 0
    assert test_env.player_attendance[player_name].weekend_attendance_count == 0
    assert test_env.player_attendance[player_name].wednesday_attendance_count == 0
    assert test_env.player_attendance[player_name].grade == "NORMAL"


def test_get_player_id(default_test_env):
    test_env = default_test_env
    assert test_env.get_player_id() == 0
    test_env.init_player("Umar")
    assert test_env.get_player_id() == 1
    test_env.init_player("Daisy")
    assert test_env.get_player_id() == 2


def test_record_player_attend_normal_day(default_test_env):
    test_env = default_test_env
    player_name = "Umar"
    attendance_day = "monday"
    test_env.record_player_attendance(player_name, attendance_day)
    assert test_env.player_attendance[player_name].attendance_point == 1
    assert test_env.player_attendance[player_name].wednesday_attendance_count == 0
    assert test_env.player_attendance[player_name].weekend_attendance_count == 0


def test_record_player_attend_wednesday(default_test_env):
    test_env = default_test_env
    player_name = "Umar"
    attendance_day = "wednesday"
    test_env.record_player_attendance(player_name, attendance_day)
    assert test_env.player_attendance[player_name].attendance_point == 3
    assert test_env.player_attendance[player_name].wednesday_attendance_count == 1
    assert test_env.player_attendance[player_name].weekend_attendance_count == 0


def test_record_player_attend_weekend(default_test_env):
    test_env = default_test_env
    player_name = "Umar"
    attendance_day = "sunday"
    test_env.record_player_attendance(player_name, attendance_day)
    assert test_env.player_attendance[player_name].attendance_point == 2
    assert test_env.player_attendance[player_name].wednesday_attendance_count == 0
    assert test_env.player_attendance[player_name].weekend_attendance_count == 1


def test_check_weekend_bonus_day(default_test_env):
    test_env = default_test_env
    player_name = "Umar"
    attendance_day = "sunday"
    for _ in range(10):
        test_env.record_player_attendance(player_name, attendance_day)
    assert test_env.player_attendance[player_name].attendance_point == 20
    test_env.check_bonus_day_count()
    assert test_env.player_attendance[player_name].attendance_point == 30


def test_check_wednesday_bonus_day_count(default_test_env):
    test_env = default_test_env
    player_name = "Umar"
    attendance_day = "wednesday"
    for _ in range(10):
        test_env.record_player_attendance(player_name, attendance_day)
    assert test_env.player_attendance[player_name].attendance_point == 30
    test_env.check_bonus_day_count()
    assert test_env.player_attendance[player_name].attendance_point == 40


def test_check_not_removed_player(default_test_env, capsys):
    test_env = default_test_env
    player_name = "Umar"
    attendance_day = "wednesday"
    test_env.record_player_attendance(player_name, attendance_day)
    test_env.check_removed_player()
    assert capsys.readouterr().out == "\nRemoved player\n==============\n"


def test_check_removed_player(default_test_env, capsys):
    test_env = default_test_env
    player_name = "Umar"
    attendance_day = "monday"
    test_env.record_player_attendance(player_name, attendance_day)
    test_env.check_removed_player()
    assert capsys.readouterr().out == f"\nRemoved player\n==============\n{player_name}\n"


def test_gold_grade_player(default_test_env, capsys):
    test_env = default_test_env
    player_name = "Umar"
    attendance_day = "wednesday"
    for _ in range(20):
        test_env.record_player_attendance(player_name, attendance_day)
    test_env.grade_player()
    assert test_env.player_attendance[player_name].grade == "GOLD"
    assert capsys.readouterr().out == f"NAME : {player_name}, POINT : 60, GRADE : GOLD\n"


def test_silver_grade_player(default_test_env, capsys):
    test_env = default_test_env
    player_name = "Umar"
    attendance_day = "wednesday"
    for _ in range(10):
        test_env.record_player_attendance(player_name, attendance_day)
    test_env.grade_player()
    assert test_env.player_attendance[player_name].grade == "SILVER"
    assert capsys.readouterr().out == f"NAME : {player_name}, POINT : 30, GRADE : SILVER\n"


def test_normal_grade_player(default_test_env, capsys):
    test_env = default_test_env
    player_name = "Umar"
    attendance_day = "wednesday"
    for _ in range(1):
        test_env.record_player_attendance(player_name, attendance_day)
    test_env.grade_player()
    assert test_env.player_attendance[player_name].grade == "NORMAL"
    assert capsys.readouterr().out == f"NAME : {player_name}, POINT : 3, GRADE : NORMAL\n"


def test_read_invalid_file(default_test_env, capsys):
    test_env = default_test_env
    test_env.run_attendance_check("./invalid_read.txt")
    assert capsys.readouterr().out == 'NAME : "VALID", POINT : 1, GRADE : NORMAL\n\nRemoved player\n==============\n"VALID"\n'

def test_run_attendance_check(default_test_env):
    test_env = default_test_env
    with patch("attendance.AttendanceManager.grade_player") as mock_func:
        test_env.run_attendance_check("./attendance_weekday_500.txt")
        mock_func.assert_called_once()

    with patch("attendance.AttendanceManager.check_bonus_day_count") as mock_func:
        test_env.run_attendance_check("./attendance_weekday_500.txt")
        mock_func.assert_called_once()

    with patch("attendance.AttendanceManager.check_removed_player") as mock_func:
        test_env.run_attendance_check("./attendance_weekday_500.txt")
        mock_func.assert_called_once()
