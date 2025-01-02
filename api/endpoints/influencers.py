from fastapi import APIRouter, HTTPException
from typing import List, Optional
from api.models.influencer import InfluencerFilter, InfluencerListResponse
import requests

router = APIRouter(
    prefix="/influencers",
    tags=["Influencers"],
    responses={404: {"description": "Not found"}}
)

# 共用的請求頭和cookies配置
HEADERS = {
    'accept': '*/*',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,da;q=0.6',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://app.euka.ai',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

COOKIES = {
    'sb-btsplwsgjvpilxywmaba-auth-token-code-verifier': '%22e8dcaf23493502d311a3eba0603082a93b5f1f8dd9e5591d317e538ec9bfc72f91249d752196e6d77cf1f329aa0750d2982ea6767cd353b0%22',
    '__stripe_mid': '93df8f3f-cf6f-4ccd-9e78-231021ca231f76abc7',
    'sb-btsplwsgjvpilxywmaba-auth-token': '%5B%22eyJhbGciOiJIUzI1NiIsImtpZCI6IjkvdHdyWllvN1ZsOFZ6czEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J0c3Bsd3NnanZwaWx4eXdtYWJhLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI1ODU2ZmZkYy0zYWQyLTRmMTQtOGI0MS04ZDdmZWIwMGM4ZjIiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM0NDEwMjU3LCJpYXQiOjE3MzQ0MDY2NTcsImVtYWlsIjoibm5kZG9vbm5uZGRvb25AZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6Im5uZGRvb25ubmRkb29uQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiI1ODU2ZmZkYy0zYWQyLTRmMTQtOGI0MS04ZDdmZWIwMGM4ZjIifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTczMzE5NTU4NX1dLCJzZXNzaW9uX2lkIjoiYzc5MzdmMjMtMDc3Yi00Mzg0LWE3NTAtNWI4OGU5NmU3Nzk0IiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.91CnepRmCwXO4AIsFegr8HM7IXD4PjRlG5u5lg0Js80%22%2C%22FP9xx_wwJ58x9HowG2ROPg%22%2Cnull%2Cnull%2Cnull%5D'
}

@router.post("/search", response_model=InfluencerListResponse)
async def search_influencers(filters: InfluencerFilter):
    """
    搜尋網紅列表，支持多種篩選條件
    
    - query: 搜尋關鍵字
    - page: 頁碼
    - per_page: 每頁數量
    - email_not_null: 是否只顯示有郵箱的網紅
    - target_categories: 目標分類列表
    - target_follower_counts: 粉絲數範圍列表 (如: ["0-20K"])
    - target_gmvs: GMV範圍列表 (如: ["$0-$100"])
    - target_gender: 性別 (可選: "Male" 或 "Female")
    - target_languages: 語言列表 (如: ["English"])
    """
    try:
        response = requests.post(
            'https://app.euka.ai/api/full-creator-search',
            cookies=COOKIES,
            headers=HEADERS,
            json=filters.as_request_params
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch influencers: {str(e)}"
        ) 