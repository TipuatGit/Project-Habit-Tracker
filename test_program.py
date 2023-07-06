from habit_class import Habit
import functions as f
##https://www.youtube.com/watch?v=WmJwA-ys39A
class TestClass:
    def add_to_database(self):
        test_habit = Habit('tesst', 'this is a test habit',
                           '14:00:30', '15:39:00', 'daily')
        
    def test_cls(self):
        f.cls()

    def test_check_database(self):
        f.check_database()

    def test_help(self):
        f.help()

    def test_check_missed_habits(self):
        f.check_missed_habits()

    def test_get_data(self):
        f.get_data()

    def test_main(self):
        f.main()

    def test_current_habits(self):
        f.current_habits()

    def test_add_new_habit(self):
        f.add_new_habit()

    def test_view_all_habits(self):
        f.view_all_habits()

    def test_my_progress(self):
        f.my_progress()

