from datetime import date

def calculate_current_school_year():
    """Calculate the current school year based on the date."""
    today = date.today()
    year = today.year
    if today.month < 7:
        return f"{year-1}/{year}"
    else:
        return f"{year}/{year+1}"

def get_school_year_choices():
    """
    Generate a list of school year choices (e.g., 2020/2021, 2021/2022, etc.).
    The list includes the current school year and the past 5 years.
    """
    current_year = date.today().year
    if date.today().month < 7:
        current_year -= 1  # Before July, consider the previous school year

    choices = []
    for i in range(6):  # Include current year and past 5 years
        start_year = current_year - i
        end_year = start_year + 1
        choices.append((f"{start_year}/{end_year}", f"{start_year}/{end_year}"))
    return choices

def calculate_actual_grade(entry_school_year, initial_grade, current_school_year):
    """
    Calculate the actual grade based on the entry school year and initial grade.
    :param entry_school_year: The year the borrower entered school (e.g., 2023/2024).
    :param initial_grade: The initial grade when the borrower started.
    :param current_school_year: The current school year (e.g., 2024/2025).
    :return: The actual grade.
    """
    # Extract the starting year from the entry school year (e.g., "2023/2024" -> 2023)
    entry_year = int(entry_school_year.split("/")[0])
    current_year = int(current_school_year.split("/")[0])

    # Calculate the difference in years and adjust the grade
    year_difference = max(0, current_year - entry_year)  # Ensure no negative grade
    return initial_grade + year_difference