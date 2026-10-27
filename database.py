import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "deskwell.db"


def get_connection():
    """Open a connection to the SQLite file. Rows behave like dictionaries."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = get_connection()
    try:
        # One settings row only (id is always 1).
        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                nickname TEXT NOT NULL DEFAULT 'Friend',
                daily_goal_breaks INTEGER NOT NULL DEFAULT 4,
                coaching_mode TEXT NOT NULL DEFAULT 'focus',
                sitting_interval_minutes INTEGER NOT NULL DEFAULT 45
            )
        """)
        # Insert the default settings row if it isn't there yet.
        conn.execute("INSERT OR IGNORE INTO settings (id) VALUES (1)")

        # Sessions table: we will start using it in the next step.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration_seconds INTEGER NOT NULL DEFAULT 0,
                posture_warnings INTEGER NOT NULL DEFAULT 0,
                breaks_completed INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()
    finally:
        conn.close()


def get_settings():
    """Return the saved settings as a dictionary."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM settings WHERE id = 1").fetchone()
        return dict(row)
    finally:
        conn.close()


def save_settings(nickname, daily_goal_breaks, coaching_mode, sitting_interval_minutes):
    """Update the single settings row."""
    conn = get_connection()
    try:
        conn.execute(
            """UPDATE settings
               SET nickname = ?, daily_goal_breaks = ?,
                   coaching_mode = ?, sitting_interval_minutes = ?
               WHERE id = 1""",
            (nickname, daily_goal_breaks, coaching_mode, sitting_interval_minutes),
        )
        conn.commit()
    finally:
        conn.close()