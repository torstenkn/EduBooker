from django.test import TestCase
from datetime import date
from .functions import get_school_year_choices, calculate_actual_grade, calculate_current_school_year
from freezegun import freeze_time

class CalculateCurrentSchoolYearTest(TestCase):

    @freeze_time("2024-06-15")
    def test_current_school_year_before_july(self):
        """Test that the current school year is correctly calculated before July."""
        expected_school_year = "2023/2024"
        self.assertEqual(calculate_current_school_year(), expected_school_year)

    @freeze_time("2024-08-15")
    def test_current_school_year_after_july(self):
        """Test that the current school year is correctly calculated after July."""
        expected_school_year = "2024/2025"
        self.assertEqual(calculate_current_school_year(), expected_school_year)

class GetSchoolYearChoicesTest(TestCase):

    @freeze_time("2024-06-15")
    def test_get_school_year_choices_before_july(self):
        """Test that the function correctly generates school years before July."""
        expected_choices = [
            ('2023/2024', '2023/2024'),
            ('2022/2023', '2022/2023'),
            ('2021/2022', '2021/2022'),
            ('2020/2021', '2020/2021'),
            ('2019/2020', '2019/2020'),
            ('2018/2019', '2018/2019')
        ]
        
        school_year_choices = get_school_year_choices()
        self.assertEqual(school_year_choices, expected_choices)

    def test_get_school_year_choices_after_july(self):
        """Test that the function correctly generates school years after July."""
        # Simulate a date after July (e.g., August 2024)
        test_date = date(2024, 8, 15)
        expected_choices = [
            ('2024/2025', '2024/2025'),
            ('2023/2024', '2023/2024'),
            ('2022/2023', '2022/2023'),
            ('2021/2022', '2021/2022'),
            ('2020/2021', '2020/2021'),
            ('2019/2020', '2019/2020')
        ]

        # Use mock.patch to simulate today's date
        with self.settings(DATE=test_date):
            school_year_choices = get_school_year_choices()

        self.assertEqual(school_year_choices, expected_choices)
        
class CalculateActualGradeTest(TestCase):

    def test_calculate_actual_grade_same_year(self):
        """Test that the actual grade is the same as the initial grade if the current school year is the same as the entry year."""
        entry_school_year = "2024/2025"
        initial_grade = 2
        current_school_year = "2024/2025"
        expected_grade = 2
        self.assertEqual(calculate_actual_grade(entry_school_year, initial_grade, current_school_year), expected_grade)

    def test_calculate_actual_grade_one_year_later(self):
        """Test that the actual grade is correctly incremented by 1 when one year has passed."""
        entry_school_year = "2023/2024"
        initial_grade = 2
        current_school_year = "2024/2025"
        expected_grade = 3
        self.assertEqual(calculate_actual_grade(entry_school_year, initial_grade, current_school_year), expected_grade)

    def test_calculate_actual_grade_two_years_later(self):
        """Test that the actual grade is correctly incremented by 2 when two years have passed."""
        entry_school_year = "2022/2023"
        initial_grade = 2
        current_school_year = "2024/2025"
        expected_grade = 4
        self.assertEqual(calculate_actual_grade(entry_school_year, initial_grade, current_school_year), expected_grade)

    def test_calculate_actual_grade_no_negative(self):
        """Test that the function does not produce a negative grade if the current year is before the entry year."""
        entry_school_year = "2024/2025"
        initial_grade = 2
        current_school_year = "2023/2024"  # Future entry year
        expected_grade = 2  # No change
        self.assertEqual(calculate_actual_grade(entry_school_year, initial_grade, current_school_year), expected_grade)