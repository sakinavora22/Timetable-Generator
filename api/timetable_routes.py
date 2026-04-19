# timetable api routes
# defines the endpoints that the frontend calls to generate timetables
# each route handles a specific action: generating schedules, listing algorithms, or health checks

from flask import Blueprint, request, jsonify
from algorithms.greedy import generate_greedy
from algorithms.backtracking import generate_backtracking
from algorithms.priority_queue import priority_queue_schedule
from algorithms.sjf import generate_sjf
from api.timetable_model import validate_subjects, normalize_subject
from utils.helpers import measure_time, get_complexity
from utils.email_sender import send_timetable_email

# create a blueprint so these routes can be registered with the main app
timetable_bp = Blueprint("timetable", __name__)


@timetable_bp.route("/send_email", methods=["POST"])
def send_email():
    try:
        data = request.json
        email = data.get("email")
        timetable = data.get("timetable")

        if not email or not timetable:
            return jsonify({"error": "email and timetable data are required"}), 400

        success, message = send_timetable_email(email, timetable)
        
        if success:
            return jsonify({"message": "email sent successfully!"})
        else:
            return jsonify({"error": f"failed to send email: {message}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# post /api/generate — takes a list of subjects and an algorithm choice,
# runs the selected scheduling algorithm, and returns the generated timetable
@timetable_bp.route("/generate", methods=["POST"])
def generate():
    # parse the json body from the request
    data = request.json

    # check that the request has the required fields
    if not data or "subjects" not in data:
        return jsonify({"error": "Missing subjects data"}), 400

    # extract subjects list, algorithm choice, and time budget from the request
    subjects = data["subjects"]
    algorithm = data.get("algorithm", "greedy")
    max_time = data.get("max_time", 20)

    # make sure at least one subject was provided
    if not subjects:
        return jsonify({"error": "No subjects provided"}), 400

    # validate the structure of each subject using the timetable model
    is_valid, error_msg = validate_subjects(subjects)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    # normalize subjects so all fields have values (fills in defaults)
    subjects = [normalize_subject(s) for s in subjects]

    # run the selected algorithm and measure how long it takes
    try:
        if algorithm == "greedy":
            result, elapsed = measure_time(generate_greedy, subjects)
        elif algorithm == "backtracking":
            result, elapsed = measure_time(generate_backtracking, subjects)
        elif algorithm == "priority_queue":
            result, elapsed = measure_time(priority_queue_schedule, subjects)
        elif algorithm == "sjf":
            result, elapsed = measure_time(generate_sjf, subjects)
        else:
            return jsonify({"error": f"Unknown algorithm: {algorithm}"}), 400
    except Exception as e:
        # catch any unexpected errors from the algorithm
        return jsonify({"error": str(e)}), 500

    # return the generated timetable along with metadata
    return jsonify({
        "timetable": result,
        "algorithm": algorithm,
        "runtime_ms": elapsed,
        "subject_count": len(subjects),
        "complexity": get_complexity(algorithm)
    })


# get /api/algorithms — returns the list of available scheduling algorithms
@timetable_bp.route("/algorithms", methods=["GET"])
def list_algorithms():
    return jsonify({
        "algorithms": [
            {"id": "greedy", "name": "Greedy Algorithm", "complexity": "O(n log n)"},
            {"id": "backtracking", "name": "Backtracking", "complexity": "O(n!)"},
            {"id": "priority_queue", "name": "Priority Queue (Heap)", "complexity": "O(n log n)"},
            {"id": "sjf", "name": "Shortest Job First", "complexity": "O(n log n)"},
        ]
    })


# get /api/health — simple check to see if the server is running
@timetable_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})
