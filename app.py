from flask import Flask, jsonify, request
import subprocess
import json
import logging
import re

app = Flask(__name__)

# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义认证 token
AUTH_TOKEN = "your_token_here"

def authenticate_token(token):
    # 验证 token 是否正确
    return token == AUTH_TOKEN

@app.route('/get_vmess_url', methods=['GET'])
def get_vmess_url():
    try:
        # 获取传递的 token
        token = request.args.get('token')

        # 验证 token
        if not authenticate_token(token):
            return jsonify({'error': 'Unauthorized'}), 401

        # 查询V2Ray端口
        port_result = subprocess.run(['v2ray', 'get-port'], capture_output=True, text=True)
        if port_result.returncode == 0:
            current_port = port_result.stdout.strip()

            # 修改V2Ray端口
            subprocess.run(['v2ray', 'port', 'VMes', current_port])
            logging.info(f'V2Ray port modified to: {current_port}')
        else:
            return jsonify({'error': 'Failed to get V2Ray port'})

        # 获取V2Ray的VMess地址
        vmess_result = subprocess.run(['v2ray', 'url'], capture_output=True, text=True)
        if vmess_result.returncode == 0:
            vmess_output = vmess_result.stdout.strip()
            logging.info(f'VMess URL obtained: {vmess_output}')
            vmess_match = re.search(r'vmess://([a-zA-Z0-9+/=]+)', vmess_output)
            vmess_url = vmess_match.group(0)

            # 将结果字典转换为 JSON 字符串
            result_json = json.dumps(vmess_url)
            logging.info(f'VMess URL obtained: {result_json}')
            return jsonify({'vmess_url': result_json})
        else:
            return jsonify({'error': 'Failed to get VMess URL'})
    except Exception as e:
        logging.error(f'Error occurred: {str(e)}')
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)