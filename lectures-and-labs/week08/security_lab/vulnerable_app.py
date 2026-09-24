"""A small note-taking API. It works. It was generated. It is not safe.

DIY 2 asks you to find three places where user input reaches storage or
output without being checked, say what an attacker could send, and fix
them.

Run it with:  python vulnerable_app.py

Nothing here is subtle or exotic. That is the point: these are the
ordinary failures that dominate generated code, and they are easy to miss
precisely because the code reads like it works -- because it does work,
right up until someone sends it something you did not expect.

DO NOT deploy this anywhere. It is teaching material.
"""
import sqlite3

DB = ":memory:"


def init(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE notes (id INTEGER PRIMARY KEY, owner TEXT, title TEXT, body TEXT)")
    conn.commit()


def add_note(conn: sqlite3.Connection, owner: str, title: str, body: str) -> None:
    """Store a note."""
    conn.execute(
        f"INSERT INTO notes (owner, title, body) VALUES ('{owner}', '{title}', '{body}')")
    conn.commit()


def search_notes(conn: sqlite3.Connection, owner: str, term: str) -> list:
    """Find a user's notes whose title contains `term`."""
    cur = conn.execute(
        f"SELECT id, title, body FROM notes WHERE owner = '{owner}' "
        f"AND title LIKE '%{term}%'")
    return cur.fetchall()


def render_note(title: str, body: str) -> str:
    """Produce the HTML fragment shown to the user."""
    return f"<div class='note'><h3>{title}</h3><p>{body}</p></div>"


def main() -> None:
    conn = sqlite3.connect(DB)
    init(conn)

    add_note(conn, "alice", "Shopping", "milk, bread")
    add_note(conn, "alice", "Passwords", "do not store passwords in notes")
    add_note(conn, "bob", "Private", "a note nobody but bob should see")

    print("alice searching for 'o':")
    for row in search_notes(conn, "alice", "o"):
        print("  ", row)

    print()
    print("rendered:")
    print(render_note("Shopping", "milk, bread"))

    conn.close()


if __name__ == "__main__":
    main()
