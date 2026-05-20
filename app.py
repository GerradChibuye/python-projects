from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary database (list)
students = [
    {
        "id": 1,
        "name": "John Banda",
        "course": "IT"
    },
    {
        "id": 2,
        "name": "Mary Phiri",
        "course": "Computer Science"
    }
]

# ---------------- GET ALL STUDENTS ----------------
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# ---------------- GET ONE STUDENT ----------------
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):

    for student in students:
        if student["id"] == id:
            return jsonify(student)

    return jsonify({"error": "Student not found"}), 404

# ---------------- ADD STUDENT ----------------
@app.route('/students', methods=['POST'])
def add_student():

    data = request.get_json()

    if not data.get("name") or not data.get("course"):
        return jsonify({"error": "Missing data"}), 400

    new_student = {
        "id": len(students) + 1,
        "name": data["name"],
        "course": data["course"]
    }

    students.append(new_student)

    return jsonify(new_student), 201

# ---------------- UPDATE STUDENT ----------------
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):

    data = request.get_json()

    for student in students:

        if student["id"] == id:

            student["name"] = data.get("name", student["name"])
            student["course"] = data.get("course", student["course"])

            return jsonify(student)

    return jsonify({"error": "Student not found"}), 404

# ---------------- DELETE STUDENT ----------------
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):

    for student in students:

        if student["id"] == id:
            students.remove(student)

            return jsonify({
                "message": "Student deleted successfully"
            })

    return jsonify({"error": "Student not found"}), 404


# ---------------- RUN SERVER ----------------
if __name__ == '__main__':
    app.run(debug=True)