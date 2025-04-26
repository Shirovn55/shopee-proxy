from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/check-cookie', methods=['POST'])
def check_cookie():
    data = request.get_json()
    cookie = data.get('cookie')

    if not cookie:
        return jsonify({'error': 'No cookie provided'}), 400

    try:
        # Gọi API get_all_order_and_checkout_list
        headers = {
            'User-Agent': 'Android app Shopee appver=28321 app_type=1',
            'Cookie': cookie,
            'Content-Type': 'application/json'
        }
        list_api = 'https://shopee.vn/api/v4/order/get_all_order_and_checkout_list?limit=5&offset=0'
        list_response = requests.get(list_api, headers=headers, timeout=10)

        if list_response.status_code != 200:
            return jsonify({'error': 'Cannot fetch order list'}), 400

        list_data = list_response.json()
        orders = list_data.get('data', {}).get('order_data', {}).get('details_list', [])

        if not orders:
            return jsonify({'error': 'No orders found'}), 404

        first_order = orders[0]
        order_id = first_order.get('info_card', {}).get('order_id')

        if not order_id:
            return jsonify({'error': 'No order_id found'}), 404

        # Gọi API get_order_detail
        detail_api = f'https://shopee.vn/api/v4/order/get_order_detail?order_id={order_id}'
        detail_response = requests.get(detail_api, headers=headers, timeout=10)

        if detail_response.status_code != 200:
            return jsonify({'error': 'Cannot fetch order detail'}), 400

        detail_data = detail_response.json()
        return jsonify(detail_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
