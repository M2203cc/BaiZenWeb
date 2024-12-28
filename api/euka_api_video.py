# import requests
# import json

# def print_response(response):
#     """格式化并打印响应数据"""
#     try:
#         print(json.dumps(response.json(), indent=2, ensure_ascii=False))
#     except:
#         print(response.text)

# # 设置认证信息
# cookies = {
#     'sb-btsplwsgjvpilxywmaba-auth-token': '%5B%22eyJhbGciOiJIUzI1NiIsImtpZCI6IjkvdHdyWllvN1ZsOFZ6czEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J0c3Bsd3NnanZwaWx4eXdtYWJhLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI1ODU2ZmZkYy0zYWQyLTRmMTQtOGI0MS04ZDdmZWIwMGM4ZjIiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM0NDA2NzYzLCJpYXQiOjE3MzQ0MDMxNjMsImVtYWlsIjoibm5kZG9vbm5uZGRvb25AZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6Im5uZGRvb25ubmRkb29uQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiI1ODU2ZmZkYy0zYWQyLTRmMTQtOGI0MS04ZDdmZWIwMGM4ZjIifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTczMzE5NTU4NX1dLCJzZXNzaW9uX2lkIjoiYzc5MzdmMjMtMDc3Yi00Mzg0LWE3NTAtNWI4OGU5NmU3Nzk0IiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.LTb9Ak6Wjlm_GpvMpkVqeOpc7d7AgzJ3I93f6taC_tA%22%2C%22B8X5qVHXw6A0sRvpp-5j4Q%22%2Cnull%2Cnull%2Cnull%5D'
# }

# headers = {
#     'accept': '*/*',
#     'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,da;q=0.6',
#     'dnt': '1',
#     'referer': 'https://app.euka.ai/content-analysis/videos',
#     'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"macOS"',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
# }

# def get_video_list(page=1, page_size=10, search=''):
#     """获取视频列表"""
#     params = {
#         'page': str(page),
#         'pageSize': str(page_size),
#     }
#     if search:
#         params['search'] = search
        
#     response = requests.get(
#         'https://app.euka.ai/api/content-analysis/videos',
#         params=params,
#         cookies=cookies,
#         headers=headers
#     )
#     return response

# def get_video_detail(video_id):
#     """获取视频详情"""
#     response = requests.get(
#         f'https://app.euka.ai/api/content-analysis/videos/{video_id}',
#         cookies=cookies,
#         headers=headers
#     )
#     return response

# def get_video_demographics(video_id):
#     """获取视频人口统计数据"""
#     params = {
#         'video-ids': str(video_id)
#     }
#     response = requests.get(
#         'https://app.euka.ai/api/content-analysis/demographics',
#         params=params,
#         cookies=cookies,
#         headers=headers
#     )
#     return response

# if __name__ == '__main__':
#     try:
#         # 1. 获取第一页视频列表
#         print("\n=== 获取视频列表 ===")
#         video_list_response = get_video_list(page=1, page_size=10)
#         print("视频列表响应：")
#         print_response(video_list_response)
        
#         if video_list_response.status_code == 200:
#             videos_data = video_list_response.json()
#             videos = videos_data.get('data', [])
            
#             if videos:
#                 print(f"\n找到 {len(videos)} 个视频")
                
#                 # 2. 获取每个视频的详细信息
#                 for i, video in enumerate(videos, 1):
#                     video_id = video.get('id') or video.get('video_id')
#                     if not video_id:
#                         print(f"\n跳过无效视频ID: {video}")
#                         continue
                        
#                     print(f"\n=== 视频 {i}: {video_id} ===")
                    
#                     # 获取视频详情
#                     print("\n--- 视频详情 ---")
#                     detail_response = get_video_detail(video_id)
#                     print_response(detail_response)
                    
#                     # 获取人口统计
#                     print("\n--- 人口统计数据 ---")
#                     demo_response = get_video_demographics(video_id)
#                     print_response(demo_response)
                    
#                     print("\n" + "="*50)
#             else:
#                 print("没有找到任何视频")
#         else:
#             print(f"获取视频列表失败: {video_list_response.status_code}")
            
#     except Exception as e:
#         print(f"发生错误: {str(e)}")
#         import traceback
#         print(traceback.format_exc()) 

