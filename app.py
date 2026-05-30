from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/get_cars")
def get_cars():

    user_id = request.args.get("user_id")

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT car_name
    FROM user_cars
    WHERE user_id = ?
    """, (str(user_id),))

    cars = cursor.fetchall()

    conn.close()

    return jsonify([car[0] for car in cars])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)