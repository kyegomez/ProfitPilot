# Path: server.py
from flask import Flask
from flask import request
from scripts.marketing_report import run_marketing_report

app = Flask(__name__)


#@app.route("/email", methods=["POST"])
#def generate_email_endpoint():
#    # Get request data
#    data = request.get_json()
#
#    # Call email generator script with data
#    result = email_endpoint(data)
#
#    # Return result
#    return result


@app.route("/report", methods=["POST"])
def marketing_report_generation():
    data = request.get_json()
    target_url = data["target_url"]

    run_marketing_report(company_path=target_url)
    with open("docs/output.txt", "r", encoding="utf-8") as f:
        output = f.read()
    return output


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
