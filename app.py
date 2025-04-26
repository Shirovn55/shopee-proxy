from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/check-cookie', methods=['POST'])
def check_cookie():
    data = request.json
    cookie = data.get('cookie')

    headers = {
        'User-Agent': 'Android app Shopee appver=28321 app_type=1',
        'Cookie': cookie,
        'Content-Type': 'application/json'
    }

    try:
        api_url = 'https://shopee.vn/api/v4/order/get_all_order_and_checkout_list?limit=10&offset=0'
        res = requests.get(api_url, headers=headers, timeout=10)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
