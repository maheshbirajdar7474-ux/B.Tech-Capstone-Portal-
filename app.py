from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
from tools import validate_team_composition, project_resource_check

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.route('/api/validate', methods=['POST'])
def validate_project():
    data = request.json
    user_prompt = data.get("prompt", "")
    
    if not user_prompt:
        return jsonify({"error": "Prompt field is empty"}), 400

    system_instructions = (
        "You are a parameters extraction engine. Read the user text proposal and extract: "
        "1. Total number of team members as an integer. "
        "2. A list of department names mentioned. "
        "3. A list of roll numbers mentioned. "
        "4. A list of software tools or cloud resources requested. "
        "Return output strictly as valid raw JSON matching this scheme: "
        '{"member_count": int, "departments": [...], "roll_numbers": [...], "resources": [...]} '
        "Do not include conversational preambles, markdown blocks, or text outside the JSON structure."
    )

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "llama3.1:8b",
            "prompt": f"{system_instructions}\n\nUser Text: {user_prompt}",
            "stream": False
        })
        
        raw_ai_output = response.json().get("response", "").strip()
        parsed_params = json.loads(raw_ai_output)
        
        member_count = parsed_params.get("member_count", 0)
        departments = parsed_params.get("departments", [])
        roll_numbers = parsed_params.get("roll_numbers", [])
        resources = parsed_params.get("resources", [])
        
        team_validation = validate_team_composition(member_count, departments, roll_numbers)
        resource_validation = project_resource_check(resources)
        
        final_response = {
            "extracted_data": {
                "member_count": member_count,
                "departments": departments,
                "roll_numbers": roll_numbers,
                "resources": resources
            },
            "team_status": team_validation,
            "resource_status": resource_validation,
            "overall_approved": (team_validation["status"] == "APPROVED" and resource_validation["all_clear"])
        }
        
        return jsonify(final_response)

    except json.JSONDecodeError:
        return jsonify({
            "error": "Failed to parse parameters correctly from the local model.",
            "raw_output_fallback": raw_ai_output if 'raw_ai_output' in locals() else ""
        }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
