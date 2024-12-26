# import requests
# import json
# from fastapi import APIRouter, Query
# import asyncio

# router = APIRouter()

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

# def get_brand_list(page=1, page_size=10, search=''):
#     """获取品牌列表"""
#     params = {
#         'page': str(page),
#         'pageSize': str(page_size),
#     }
#     if search:
#         params['search'] = search
        
#     response = requests.get(
#         'https://app.euka.ai/api/content-analysis/brands',
#         params=params,
#         cookies=cookies,
#         headers=headers
#     )
#     return response

# def fetch_brand_detail(brand_id):
#     """获取品牌详情"""
#     response = requests.get(
#         f'https://app.euka.ai/api/content-analysis/brands/{brand_id}',
#         cookies=cookies,
#         headers=headers
#     )
#     return response

# def get_brand_demographics(brand_id):
#     """获取品牌人口统计数据"""
#     params = {
#         'brand-ids': str(brand_id)
#     }
#     response = requests.get(
#         'https://app.euka.ai/api/content-analysis/demographics',
#         params=params,
#         cookies=cookies,
#         headers=headers
#     )
#     return response

# def get_brand_products(brand_id, page=1, page_size=10):
#     """获取品牌产品列表"""
#     params = {
#         'brand-ids': str(brand_id),
#         'page': str(page),
#         'pageSize': str(page_size)
#     }
#     response = requests.get(
#         'https://app.euka.ai/api/content-analysis/products',
#         params=params,
#         cookies=cookies,
#         headers=headers
#     )
#     return response

# def get_brand_videos(brand_id, page=1, page_size=10):
#     """获取品牌视频列表"""
#     params = {
#         'brand-ids': str(brand_id),
#         'page': str(page),
#         'pageSize': str(page_size)
#     }
#     response = requests.get(
#         'https://app.euka.ai/api/content-analysis/videos',
#         params=params,
#         cookies=cookies,
#         headers=headers
#     )
#     return response

# @router.get("/brands")
# async def get_brands(
#     page: int = Query(1, description="Page number"),
#     pageSize: int = Query(10, description="Items per page"),
#     search: str = Query(None, description="Search query")
# ):
#     response = get_brand_list(page=page, page_size=pageSize, search=search)
#     if response.status_code == 200:
#         data = response.json()
#         formatted_data = {
#             "data": [
#                 {
#                     "id": item.get("seller_id"),
#                     "name": item.get("name"),
#                     "brand_url": item.get("brand_url"),
#                     "num_products": item.get("num_products"),
#                     "total_sales": item.get("total_sales")
#                 }
#                 for item in data.get("data", [])
#             ],
#             "total": data.get("total", 0)
#         }
#         return formatted_data
#     return response.json()

# @router.get("/brands/{brand_id}")
# async def get_brand_detail(brand_id: str):
#     response = fetch_brand_detail(brand_id)
#     return response.json()

# async def main():
#     try:
#         print("\n=== 获取品牌列表 ===")
#         brand_list_response = get_brand_list(page=1, page_size=10)
#         print("品牌列表响应：")
#         print_response(brand_list_response)
        
#         if brand_list_response.status_code == 200:
#             brands_data = brand_list_response.json()
#             brands = brands_data.get('data', [])
#             total_brands = brands_data.get('total', 0)
            
#             if brands:
#                 print(f"\n当前页找到 {len(brands)} 个品牌, 总共有 {total_brands} 个品牌")
#                 print(f"当前页码: 1, 每页显示: 10")
                
#                 for i, brand in enumerate(brands, 1):
#                     brand_id = brand.get('seller_id')
#                     if not brand_id:
#                         print(f"\n跳过无效品牌ID: {brand}")
#                         continue
                        
#                     print(f"\n=== 品牌 {i}: {brand.get('name', 'Unknown')} ({brand_id}) ===")
                    
#                     print("\n--- 品牌详情 ---")
#                     detail_response = fetch_brand_detail(brand_id)
#                     print_response(detail_response)
                    
#                     print("\n--- 人口统计数据 ---")
#                     demo_response = get_brand_demographics(brand_id)
#                     print_response(demo_response)
                    
#                     print("\n--- 产品列表 ---")
#                     products_response = get_brand_products(brand_id)
#                     print_response(products_response)
                    
#                     print("\n--- 视频列表 ---")
#                     videos_response = get_brand_videos(brand_id)
#                     print_response(videos_response)
                    
#                     print("\n" + "="*50)
#             else:
#                 print("没有找到任何品牌")
#         else:
#             print(f"获取品牌列表失败: {brand_list_response.status_code}")
            
#     except Exception as e:
#         print(f"发生错误: {str(e)}")
#         import traceback
#         print(traceback.format_exc())

# if __name__ == '__main__':
#     asyncio.run(main())