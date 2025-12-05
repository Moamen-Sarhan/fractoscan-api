import sqlite3

def create_db():
    conn = sqlite3.connect("fractoscan.db")
    cursor = conn.cursor()

    # ----------------------
    # USERS TABLE
    # ----------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE,
            password TEXT NOT NULL  -- يجب تخزين هاش بدلاً من النص العادي
        )
    """)

    # ----------------------
    # XRAY IMAGE TABLE
    # ----------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS xray_image (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_data BLOB NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    """)

    # ----------------------
    # AI ANALYSIS TABLE
    # ----------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_analysis (
            analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (image_id) REFERENCES xray_image(image_id) ON DELETE CASCADE
        )
    """)

    # ----------------------
    # REPORT TABLE
    # ----------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS report (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            report TEXT,
            FOREIGN KEY (analysis_id) REFERENCES ai_analysis(analysis_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print("Database and tables created successfully ✔")

# Run function
if __name__ == "__main__":
    create_db()
