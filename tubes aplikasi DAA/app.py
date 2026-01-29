from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error
import time

app = Flask(__name__)

# =============================
# KONFIGURASI DATABASE
# =============================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "skripsi_db"
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print("Database error:", e)
    return None


# =============================
# STRING MATCHING
# =============================
def string_matching(text, pattern):
    return pattern.lower() in text.lower()


# =============================
# ROUTE UTAMA
# =============================
@app.route("/", methods=["GET", "POST"])
def index():
    hasil = []
    keyword = ""
    times = []
    rata_rata = 0

    if request.method == "POST":
        keyword = request.form["keyword"]

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT judul, penulis, tahun FROM skripsi")
            data = cursor.fetchall()

            # =============================
            # PENGUJIAN WAKTU 10x PERCOBAAN
            # =============================
            for row in data:
                 string_matching(row["judul"], keyword)

            # pengujian 10x
            for _ in range(10):
                start_time = time.perf_counter()

                hasil_temp = []
                for row in data:
                    if string_matching(row["judul"], keyword):
                     hasil_temp.append(row)

                end_time = time.perf_counter()
                times.append(end_time - start_time)

            hasil = hasil_temp
            rata_rata = round(sum(times) / 10, 6)

            cursor.close()
            conn.close()
        else:
            print("Koneksi database gagal")

    return render_template(
        "index.html",
        hasil=hasil,
        keyword=keyword,
        times=times,
        rata_rata=rata_rata
    )


# =============================
# MAIN
# =============================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)