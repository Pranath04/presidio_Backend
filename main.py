from flask import Flask, request, jsonify

app = Flask(__name__)
import json

#TEACHERS_FILE = 'teachers.json'
TEACHERS_FILE = r"D:\presido\teachers.json"


def read_teachers():
    try:
        with open(TEACHERS_FILE, 'r') as file:
            teachers_data = json.load(file)
        return teachers_data
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []

def write_teachers(teachers_data):
    try:
        with open(TEACHERS_FILE, 'w') as file:
            json.dump(teachers_data, file, indent=2)
            return jsonify({"success":"Data inserted successfully"}),200
    except:
        return jsonify({"Error":"Some thing went wrong"}),400

@app.route('/show_teachers', methods=['GET'])
def show_teachers():
    return read_teachers()
    
@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    data = request.get_json()
    # Validate required fields
    if 'full_name' not in data or 'age' not in data or 'dob' not in data or 'num_classes' not in data:
        return jsonify({"error": "Expected keys  i.e., full_name, age,dob,num_classes in the JSON Data"}), 400
    teachers_data = read_teachers()
    # Generate a unique ID for the new teacher
    new_teacher_id = max([t.get('id', 0) for t in teachers_data], default=0) + 1

    new_teacher = {
        "id": new_teacher_id,
        "full_name": data['full_name'],
        "age": data["age"],
        "dob": data["dob"],
        "num_classes": data["num_classes"]
    }

    teachers_data.append(new_teacher)
    return write_teachers(teachers_data)

@app.route('/delete_teacher/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    teachers=read_teachers()
    try:
        # Find the teacher by ID
        teacher = next((t for t in teachers if t["id"] == id), None)

        if teacher:
            # Remove the teacher's record
            modified_teachers = [t for t in teachers if t["id"] != id]
            write_teachers(modified_teachers)
            return jsonify({"message": f"Teacher with ID {id} deleted successfully"})
        else:
            return jsonify({"error": f"Teacher with ID {id} not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update_teacher/<int:id>', methods=['PUT'])
def update_teacher(id):
    data = request.get_json()

    # Validate required fields
    if 'full_name' not in data or 'age' not in data or 'dob' not in data or 'num_classes' not in data:
        return jsonify({"error": "Expected keys  i.e., full_name, age,dob,num_classes in the JSON Data"}), 400

    teachers = read_teachers()
    try:
        # Find the teacher by ID
        teacher = next((t for t in teachers if t["id"] == id), None)
        if teacher:
            # Remove the updated teacher's record
            modified_teachers = [t for t in teachers if t["id"] != id]

            update_teacher = {
                "id": id,
                "full_name": data['full_name'],
                "age": data["age"],
                "dob": data["dob"],
                "num_classes": data["num_classes"]
            }

            modified_teachers.append(update_teacher)
            write_teachers(modified_teachers)
            return jsonify({"message": f"Teacher with ID {id} updated successfully"})
        else:
            return jsonify({"error": f"Teacher with ID {id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search_teachers/<name>', methods=['GET'])
def search_teachers(name):
    teachers = read_teachers()
    filtered_teacher = next((t for t in teachers if t["full_name"] == name),None)
    if filtered_teacher is None:
        return jsonify({"Success":"No data found"}),200
    else:
        return filtered_teacher

@app.route('/filtered_criteria', methods=['GET'])
def filtered_criteria():
    data = request.get_json()

    # Validate required fields
    if 'age' not in data and 'num_classes' not in data:
        return jsonify({"error": "Expected keys ie., age or num_classes"}), 404

    teachers = read_teachers()
    if 'age' in data and 'num_classes' in data:    
        filtered_teacher = next((t for t in teachers if t["age"] == data['age'] and t["num_classes"] == data['num_classes']), None)
    else:
        if 'age' in data:
            filtered_teacher = next((t for t in teachers if t["age"] == data['age']), None)
        else:
            filtered_teacher = next((t for t in teachers if t["num_classes"] == data['num_classes']), None)

    if filtered_teacher is None:
        return jsonify({"Success":"No data found"}),200
    else:
        return filtered_teacher
if __name__ == '__main__':
    app.run(debug=True)