import sqlite3

#get DB connection
def get_connection():
    conn = sqlite3.connect('hats.db', check_same_thread=False)
    return conn

# Run this once to setup the table
def setup_db():
    try:
        conn = get_connection()
        conn.execute("CREATE TABLE IF NOT EXISTS inventory (name TEXT, qty TEXT)")
        # Add some dummy data
        conn.execute("INSERT INTO inventory VALUES ('Red Cap', '50')")
        conn.execute("INSERT INTO inventory VALUES ('Blue Beanie', '10')")
        conn.commit()
        conn.close()
        print("Database initialized!")
    except Exception as e:
        print("Setup error: " + str(e))