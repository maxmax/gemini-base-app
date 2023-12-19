import os
from flask import Flask, request, jsonify
import requests
import json


app = Flask(__name__)


# Set your Gemini API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


@app.route("/")
def list_projects():
    """
    List all projects in your Gemini account.
    """
    url = "https://api.gemini.com/v1/account/projects"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    response = requests.get(url, headers=headers)

    try:
        projects = response.json()
        return json.dumps(projects, indent=4)
    except JSONDecodeError as e:
        return f"Error decoding JSON: {e}"


## http://localhost:5000/metrics?project_id=YOUR_PROJECT_ID
@app.route("/metrics")
def get_metrics():
    """
    Get metrics for a specific Gemini project.
    """
    project_id = request.args.get("project_id")
    if not project_id:
        return "Missing project_id parameter", 400

    url = f"https://api.gemini.com/v1/projects/{project_id}/metrics"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    response = requests.get(url, headers=headers)

    try:
        metrics = response.json()
        return json.dumps(metrics, indent=4)
    except JSONDecodeError as e:
        return f"Error decoding JSON: {e}", 500


if __name__ == "__main__":
    app.run(debug=True)
