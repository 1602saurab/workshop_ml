import sqlite3


DB_NAME = "clinic.db"


def init_db():

    con = sqlite3.connect(DB_NAME)

    cur = con.cursor()

    # Doctors table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY,
            name TEXT,
            specialization TEXT,
            timing TEXT
        )
    """)

    # Patients table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            city TEXT,
            blood_group TEXT
        )
    """)

    # Sample doctors
    cur.execute("SELECT COUNT(*) FROM doctors")

    if cur.fetchone()[0] == 0:

        cur.executemany(
            """
            INSERT INTO doctors
            (id, name, specialization, timing)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    1,
                    "Dr. Sharma",
                    "General Physician",
                    "10 AM - 2 PM"
                ),
                (
                    2,
                    "Dr. Mehta",
                    "Cardiologist",
                    "4 PM - 8 PM"
                ),
            ]
        )

    # Sample patients
    cur.execute("SELECT COUNT(*) FROM patients")

    if cur.fetchone()[0] == 0:

        cur.executemany(
            """
            INSERT INTO patients
            (id, name, age, city, blood_group)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    1,
                    "Rahul Sharma",
                    32,
                    "Jaipur",
                    "B+"
                ),
                (
                    2,
                    "Priya Verma",
                    28,
                    "Jaipur",
                    "O+"
                ),
                (
                    3,
                    "Amit Singh",
                    45,
                    "Ajmer",
                    "A+"
                ),
            ]
        )

    con.commit()
    con.close()


def get_doctor(name: str):

    con = sqlite3.connect(DB_NAME)

    cur = con.cursor()

    cur.execute(
        """
        SELECT id, name, specialization, timing
        FROM doctors
        WHERE LOWER(name) = LOWER(?)
        """,
        (name,)
    )

    result = cur.fetchone()

    con.close()

    return result


def get_patient(patient_id: int):

    con = sqlite3.connect(DB_NAME)

    cur = con.cursor()

    cur.execute(
        """
        SELECT id, name, age, city, blood_group
        FROM patients
        WHERE id = ?
        """,
        (patient_id,)
    )

    result = cur.fetchone()

    con.close()

    return result