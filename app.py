from flask import Flask, request, jsonify
import os
import requests
import json

API_KEY = os.environ.get("GEMINI_API_KEY")

app = Flask(__name__)

@app.route('/api-info', methods=["GET"])
def api_info():
    return jsonify({"test": "Привіт 🦝"})

@app.route("/", methods=["GET"])
def list_projects():
    """
    List all projects in your Gemini account.
    """
    url = "https://api.gemini.com/v1/account/projects"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)

    try:
        projects = response.json()
        return json.dumps(projects, indent=4)
    except JSONDecodeError as e:
        return f"Error decoding JSON: {e}"


# /metrics?project_id=YOUR_PROJECT_ID
@app.route("/metrics", methods=["GET"])
def get_metrics():
    """
    Get metrics for a specific Gemini project.
    """
    project_id = request.args.get("project_id")
    if not project_id:
        return "Missing project_id parameter", 400

    url = f"https://api.gemini.com/v1/projects/{project_id}/metrics"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)

    try:
        metrics = response.json()
        return json.dumps(metrics, indent=4)
    except JSONDecodeError as e:
        return f"Error decoding JSON: {e}", 500


@app.route("/get-haiku", methods=["GET"])
def get_generated_bison():
    # Predefined test prompt
    prompt = "Write a Japanese poem in haiku style."

    # Specify the model to use
    model_id = "text-bison-001"  # Replace with any of the available models mentioned above
    # text-bison-001, text-bison-002, text-bison-003, text-bison-004

    # Create a request to the API
    url = "https://generativelanguage.googleapis.com/v1beta2/models/{}:generateText?key={}".format(model_id, API_KEY)
    headers = {"Content-Type": "application/json"}
    body = {"prompt": {"text": prompt}}

    # Send a request to the API
    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        return jsonify({"error": "Error generating text"}), response.status_code

    result = response.json()
    generated_text = result["candidates"][0]["output"]

    return jsonify({"generated_text": generated_text})

# /get-prompts?lang=En&prompt="Write a haiku about nature"
@app.route("/get-prompts", methods=["GET"])
def get_prompts():
    # Get the language and prompt from the query parameters
    lang = request.args.get("lang")
    prompt = request.args.get("prompt")

    # Validate the language
    if lang not in ["En", "Ja", "Ua"]:
        return jsonify({"error": "Invalid language"}), 400

    # Generate the prompt based on the language
    if lang == "En":
        prompt = "Write an English poem in haiku style."
    elif lang == "Ja":
        prompt = "日本語の俳句スタイルで詩を書いてください。"
    elif lang == "Ua":
        prompt = "Напишіть вірш у стилі хайку українською мовою."

    # Specify the model to use based on the language
    if lang == "En":
        model_id = "text-bison-001"
    elif lang == "Ja":
        model_id = "text-bison-002"
    elif lang == "Ua":
        model_id = "text-bison-003"

    # Create a request to the API
    url = "https://generativelanguage.googleapis.com/v1beta2/models/{}:generateText?key={}".format(model_id, API_KEY)
    headers = {"Content-Type": "application/json"}
    body = {"prompt": {"text": prompt}}

    # Send a request to the API
    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        return jsonify({"error": "Error generating text"}), response.status_code

    result = response.json()
    generated_text = result["candidates"][0]["output"]

    return jsonify({"generated_text": generated_text})


if __name__ == "__main__":
    app.run()
