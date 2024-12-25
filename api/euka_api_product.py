import requests
import json

def print_response(response):
    """格式化并打印响应数据"""
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)

# 设置认证信息
cookies = {
    '_gcl_au': '1.1.582945540.1733194843',
    'sb-btsplwsgjvpilxywmaba-auth-token-code-verifier': '807490b7f6d8da29ccab83a74d05eda28238402a7afb7f8398d08740416dd34ff4c26f0787fc9a20b82c471d4b2ecb933f076e8b77b02980',
    'sb-btsplwsgjvpilxywmaba-auth-token': '["eyJhbGciOiJIUzI1NiIsImtpZCI6IjkvdHdyWllvN1ZsOFZ6czEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J0c3Bsd3NnanZwaWx4eXdtYWJhLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI1NzhjYmI1YS0wN2U2LTQ4MTctYjI3Ni1hNWI3ZWJkZjU4ODkiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM0OTM3MjQ3LCJpYXQiOjE3MzQ5MzM2NDcsImVtYWlsIjoibTIyMDNjQHByb3Rvbi5tZSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJtMjIwM2NAcHJvdG9uLm1lIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6IjU3OGNiYjVhLTA3ZTYtNDgxNy1iMjc2LWE1YjdlYmRmNTg4OSJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzMzMTk0ODUzfV0sInNlc3Npb25faWQiOiI4MDZhZTY3NC0yZDhlLTQxODctYjE5Yi00MzBlYTFjZDc2OTkiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.j06DTqs7cd9HyHoJUx-ilzIoZF3W7iDnTJHm0SzV4fE","pQ5Cfu_W5ettVg6ZW8MPZQ",null,null,null]'
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'dnt': '1',
    'referer': 'https://app.euka.ai/content-analysis/products',
    'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def get_product_list(page=1, page_size=10, with_images=True, from_origin=True):
    """获取产品列表"""
    params = {
        'page': str(page),
        'pageSize': str(page_size),
        'with-images': str(with_images).lower(),
        'from-origin': str(from_origin).lower()
    }
    response = requests.get(
        'https://app.euka.ai/api/content-analysis/products',
        params=params,
        cookies=cookies,
        headers=headers
    )
    return response

def get_product_detail(product_id):
    """获取产品详情"""
    response = requests.get(
        f'https://app.euka.ai/api/content-analysis/products/{product_id}',
        cookies=cookies,
        headers=headers
    )
    return response

def get_product_demographics(product_id):
    """获取产品人口统计数据"""
    params = {
        'product-ids': str(product_id)
    }
    response = requests.get(
        'https://app.euka.ai/api/content-analysis/demographics',
        params=params,
        cookies=cookies,
        headers=headers
    )
    return response

def get_product_videos(product_id, page=1, page_size=10, start_date=None, end_date=None):
    """获取产品相关视频"""
    params = {
        'product-ids': str(product_id),
        'page': str(page),
        'pageSize': str(page_size)
    }
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
        
    response = requests.get(
        'https://app.euka.ai/api/content-analysis/videos',
        params=params,
        cookies=cookies,
        headers=headers
    )
    return response

if __name__ == '__main__':
    try:
        # 1. 获取产品列表
        print("获取产品列表：")
        product_list_response = get_product_list()
        print_response(product_list_response)
        
        # 确保响应成功并包含数据
        if product_list_response.status_code == 200:
            products_data = product_list_response.json()
            
            if 'data' in products_data and products_data['data']:
                # 遍历每个产品
                for product in products_data['data']:
                    # 使用正确的 ID 字段
                    product_id = product.get('product_id')  # 或者根据实际返回数据结构调整
                    
                    if product_id:
                        print(f"\n处理产品 ID: {product_id}")
                        
                        # 2. 获取产品详情
                        print("\n获取产品详情：")
                        product_detail_response = get_product_detail(product_id)
                        if product_detail_response.status_code == 200:
                            print_response(product_detail_response)
                        else:
                            print(f"获取产品详情失败: {product_detail_response.status_code}")
                        
                        # 3. 获取产品人口统计
                        print("\n获取产品人口统计：")
                        demographics_response = get_product_demographics(product_id)
                        if demographics_response.status_code == 200:
                            print_response(demographics_response)
                        else:
                            print(f"获取人口统计失败: {demographics_response.status_code}")
                        
                        # 4. 获取产品相关视频
                        print("\n获取产品相关视频：")
                        videos_response = get_product_videos(product_id)
                        if videos_response.status_code == 200:
                            print_response(videos_response)
                        else:
                            print(f"获取相关视频失败: {videos_response.status_code}")
                        
                        print("\n" + "="*50 + "\n")  # 分隔线
                    else:
                        print(f"产品数据中未找到有效的 ID: {product}")
            else:
                print("产品列表为空或格式不正确")
        else:
            print(f"获取产品列表失败: {product_list_response.status_code}")
            
    except Exception as e:
        print(f"发生错误: {str(e)}")
        # 打印更详细的错误信息
        import traceback
        print(traceback.format_exc())

