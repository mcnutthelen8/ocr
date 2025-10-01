from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

IPQS_KEY = "BEPgiVi4XCx0URXqigTXonNwsLbkRdez"  # <-- Replace with your IPQS key

def ipqs_lookup(ip: str) -> dict:
    """
    Check if an IP is VPN/proxy using IPQualityScore.
    """
    url = f"https://ipqualityscore.com/api/json/ip/{IPQS_KEY}/{ip}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("success", False):
            return {"success": False}

        return {
            "proxy": data.get("proxy", False),
            "vpn": data.get("vpn", False),
            "fraud_score": data.get("fraud_score", 0),
            "success": True
        }

    except requests.RequestException as e:
        return {"error": str(e), "success": False}

@app.route("/")
def home():
    return "IPQS VPN/Proxy Checker API"

@app.route("/check_ip", methods=["GET"])
def check_ip():
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Please provide an IP address using ?ip=IP_ADDRESS"}), 400

    result = ipqs_lookup(ip)

    if "error" in result:
        return jsonify(result), 500

    if not result.get("success", False):
        status = "API issue"
    elif not result["proxy"] and not result["vpn"] and result["fraud_score"] <= 75:
        status = "Valid"
    else:
        status = "VPN detect"

    return jsonify({
        "ip": ip,
        "proxy": result.get("proxy", None),
        "vpn": result.get("vpn", None),
        "fraud_score": result.get("fraud_score", None),
        "status": status
    })

if __name__ == "__main__":
    app.run(debug=True)
