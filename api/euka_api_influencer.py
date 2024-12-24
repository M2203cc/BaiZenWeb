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
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://app.euka.ai',
    'referer': 'https://app.euka.ai/influencers',
    'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def search_influencers(
    query='',
    page=1,
    per_page=10,
    email_not_null=False,
    target_categories=None,
    target_follower_counts=None,
    target_gmvs=None,
    target_gender=None,
    target_languages=None
):
    """搜索影响者"""
    json_data = {
        'query': query,
        'page': page,
        'perPage': per_page,
        'emailNotNull': email_not_null
    }
    
    if target_categories:
        json_data['targetCategories'] = target_categories
    if target_follower_counts:
        json_data['targetFollowerCounts'] = target_follower_counts
    if target_gmvs:
        json_data['targetGMVs'] = target_gmvs
    if target_gender:
        json_data['targetGender'] = target_gender
    if target_languages:
        json_data['targetLanguages'] = target_languages

    response = requests.post(
        'https://app.euka.ai/api/full-creator-search',
        cookies=cookies,
        headers=headers,
        json=json_data
    )
    return response

if __name__ == '__main__':
    # 示例使用
    print("搜索影响者：")
    search_params = {
        'target_categories': ['Textiles & Soft Furnishings'],
        'target_follower_counts': ['0-20K'],
        'target_gmvs': ['$0-$100'],
        'target_gender': 'Male',
        'target_languages': ['English']
    }
    
    influencer_response = search_influencers(**search_params)
    print_response(influencer_response)