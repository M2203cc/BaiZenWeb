import requests
import json

# 定义一个函数来格式化响应数据
def print_response(response):
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)

# 设置你的认证信息
cookies = {
    '_gcl_au': '1.1.582945540.1733194843',
    'sb-btsplwsgjvpilxywmaba-auth-token-code-verifier': '807490b7f6d8da29ccab83a74d05eda28238402a7afb7f8398d08740416dd34ff4c26f0787fc9a20b82c471d4b2ecb933f076e8b77b02980',
    'sb-btsplwsgjvpilxywmaba-auth-token': '["eyJhbGciOiJIUzI1NiIsImtpZCI6IjkvdHdyWllvN1ZsOFZ6czEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J0c3Bsd3NnanZwaWx4eXdtYWJhLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI1NzhjYmI1YS0wN2U2LTQ4MTctYjI3Ni1hNWI3ZWJkZjU4ODkiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM0OTM3MjQ3LCJpYXQiOjE3MzQ5MzM2NDcsImVtYWlsIjoibTIyMDNjQHByb3Rvbi5tZSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJtMjIwM2NAcHJvdG9uLm1lIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6IjU3OGNiYjVhLTA3ZTYtNDgxNy1iMjc2LWE1YjdlYmRmNTg4OSJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzMzMTk0ODUzfV0sInNlc3Npb25faWQiOiI4MDZhZTY3NC0yZDhlLTQxODctYjE5Yi00MzBlYTFjZDc2OTkiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.j06DTqs7cd9HyHoJUx-ilzIoZF3W7iDnTJHm0SzV4fE","pQ5Cfu_W5ettVg6ZW8MPZQ",null,null,null]',
    'ph_phc_gFx2zFM1NeHLt1CdZ9RZSBmAau5TYiVWtMPF7l8pMwg_posthog': '{"distinct_id":"01938a76-815e-7146-8c62-fe320043e30c","$sesid":[1734936629828,"0193f22b-2a40-7eb3-91ea-9e70fab8035a",1734934735424]}'
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'dnt': '1',
    'referer': 'https://app.euka.ai/content-analysis/videos',
    'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def get_video_list(page=1, page_size=10, search='', brand='', product='', view_count=''):
    """获取视频列表"""
    params = {
        'page': str(page),
        'pageSize': str(page_size),
        'search': search,
    }
    
    # 添加筛选参数
    if brand:
        params['brand'] = brand
    if product:
        params['product'] = product
    if view_count:
        params['viewCount'] = view_count
        
    response = requests.get(
        'https://app.euka.ai/api/content-analysis/videos',
        params=params,
        cookies=cookies,
        headers=headers
    )
    return response

def get_video_detail(video_id):
    """获取特定视频详情"""
    response = requests.get(
        f'https://app.euka.ai/api/content-analysis/videos/{video_id}',
        cookies=cookies,
        headers=headers
    )
    return response

def get_video_demographics(video_id):
    """获取视频人口统计数据"""
    params = {
        'video-ids': str(video_id),
    }
    response = requests.get(
        'https://app.euka.ai/api/content-analysis/demographics',
        params=params,
        cookies=cookies,
        headers=headers
    )
    return response

if __name__ == '__main__':
    # 1. 获取视频列表
    print("获取视频列表：")
    video_list_response = get_video_list()
    print_response(video_list_response)
    
    # 如果成功获取视频列表，获取第一个视频的详细信息
    try:
        video_id = video_list_response.json()['data'][0]['id']
        
        # 2. 获取特定视频详情
        print("\n获取视频详情：")
        video_detail_response = get_video_detail(video_id)
        print_response(video_detail_response)
        
        # 3. 获取视频人口统计数据
        print("\n获取视频人口统计数据：")
        demographics_response = get_video_demographics(video_id)
        print_response(demographics_response)
        
    except Exception as e:
        print(f"发生错误: {str(e)}") 

