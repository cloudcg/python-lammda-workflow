import json
import urllib.request
import urllib.error

def lambda_handler(event, context):
    try:
        # 构建 Flask 应用程序的 URL
        flask_app_url = "http://{ip}:{port}/get_vmess_url"  # 替换为您 Flask 应用程序的公共 IP 地址

        # 替换为您的认证 token
        token = "your_token_here"

        # 构建带有 token 的请求 URL
        full_url = f"{flask_app_url}?token={token}"

        # 发送 GET 请求
        response = urllib.request.urlopen(full_url)

        # 检查响应状态码
        if response.status == 200:
            # 从响应中读取数据并解码为 JSON
            response_data = response.read().decode('utf-8')
            response_json = json.loads(response_data)

            # 从响应中提取 VMess 地址
            vmess_url_full = response_json.get('vmess_url')

            # 从完整的 URL 中提取 VMess 部分
            if vmess_url_full:
                vmess_url = vmess_url_full.split('"')[1]
                return {
                    'statusCode': 200,
                    'body': json.dumps({'vmess_url': vmess_url})
                }
            else:
                return {
                    'statusCode': 500,
                    'body': json.dumps({'error': 'Failed to extract VMess URL'})
                }
        else:
            return {
                'statusCode': response.status,
                'body': json.dumps({'error': 'Failed to fetch VMess URL'})
            }
    except urllib.error.URLError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }