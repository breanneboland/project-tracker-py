"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.
    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    pass


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    QUERY = """
    SELECT title, description, max_grade
    FROM Projects
    WHERE title = ?
    """
    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()
    print "Project: %s - %s and has a maximum grade of %s." % (
        row[0], row[1], row[2])



def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """
    SELECT grade, student_github, project_title FROM grades
    WHERE student_github = ? AND project_title = ?
    """

    db_cursor.execute(QUERY, (github, title))
    row = db_cursor.fetchone()
    print "Grade for %s project by %s github was %s." % (row[2], row[1], row[0])


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """
    INSERT INTO Grades (student_github, project_title, grade) VALUES (?, ?, ?);
    """
    db_cursor.execute(QUERY, (github, title, grade))

    QUERY2 = """
    SELECT student_github, project_title, grade) FROM Grades WHERE student_github = ? AND project_title = ?;
    """
    db_cursor.execute(QUERY2, (github, title))
    row = db_cursor.fetchone()
    print "Github user %s received a %s on project %s." % (row[0], row[2], row[1])

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
