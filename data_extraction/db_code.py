"""This module contains the code to interact with the database."""

import csv
import sqlite3


class EmploymentSituationDB:
    """Class to interact  with the employment_situation table in the database."""

    def __init__(self, db_filename: str) -> None:
        """Initialize the database connection and create table if it doesn't exist."""
        self.db_filename = db_filename
        self.conn = sqlite3.connect(self.db_filename)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self) -> None:
        """Create the employment_situation table if it doesn't exist."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employment_situation (
                id INTEGER PRIMARY KEY,
                text_column TEXT,
                date_column TEXT,
                updated_date TEXT
            )
            """
        )
        self.conn.commit()

    def save_to_db(self, text: str, date_column: str) -> None:
        """Save data to the database."""
        self.cursor.execute(
            """
            INSERT INTO employment_situation (text_column, date_column)
            VALUES (?, ?)
            """,
            (text, date_column),
        )
        self.conn.commit()

    def update_from_csv(self, csv_filename: str) -> None:
        """Read from CSV and update the updated_date column using the id as the index."""
        with open(csv_filename, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for index, row in enumerate(reader, start=1):  # Use enumerate to get the id
                updated_date = row[0]
                # Update the record where id matches the index
                self.cursor.execute(
                    """
                    UPDATE employment_situation
                    SET updated_date = ?
                    WHERE id = ?
                    """,
                    (updated_date, index),
                )
                print("Updated id:", index, "with updated_date:", updated_date)
        self.conn.commit()

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()


if __name__ == "__main__":
    db = EmploymentSituationDB("tests_db/main.db")
    csv_filename = "first_fridays.csv"
    db.update_from_csv(csv_filename)
    db.close()
