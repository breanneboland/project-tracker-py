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
    if row == None:
        print "Student not found. Try again."
    else:
        print "Student: %s %s\nGithub account: %s" % (
            row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.
    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    QUERY = """INSERT INTO Students (first_name, last_name, github) 
            VALUES (?, ?, ?)
            """
    db_cursor.execute(QUERY, (first_name, last_name, github))
    db_connection.commit()

    get_student_by_github(github)


def make_new_project(project_title, project_description, max_grade):
    QUERY = """INSERT INTO Projects (title, description, max_grade) 
        VALUES (?, ?, ?)
    """
    db_cursor.execute(QUERY, (project_title, project_description, max_grade))
    db_connection.commit()

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

def get_all_grades(student_github):
    QUERY = """SELECT first_name, last_name, project_title, grade 
            FROM  Students JOIN Grades
            ON (grades.student_github = students.github)
    """
    db_cursor.execute(QUERY, (student_github, ))
    results = db_cursor.fetchall()
    print results

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
    db_connection.commit()
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
            if len(args) == 1:
                github = args[0]
                get_student_by_github(github)
            else:
                print "Too many arguments, please provide only github username you are seeking"

        elif command == "new_student":
            if len(args) == 3:
                first_name, last_name, github = args   # unpack!
                make_new_student(first_name, last_name, github)
            else:
                print "Need all student info - first name, last name and github username."


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
