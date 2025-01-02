from fastapi import APIRouter, HTTPException
from typing import List, Optional
from api.models.category import (
    CategoryListResponse,
    CategoryDetailResponse,
    CategoryBrandsResponse
)
import requests

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={404: {"description": "Category not found"}}
)

# 共用的請求頭和cookies配置
HEADERS = {
    'accept': '*/*',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,da;q=0.6',
    'dnt': '1',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'x-client-info': '@supabase/auth-helpers-nextjs@0.9.0',
    'x-supabase-api-version': '2024-01-01',
    'Cache-Control': 'no-cache'  # 保證每次都獲取最新資訊
}

COOKIES = {
    'sb-btsplwsgjvpilxywmaba-auth-token-code-verifier': '%22e8dcaf23493502d311a3eba0603082a93b5f1f8dd9e5591d317e538ec9bfc72f91249d752196e6d77cf1f329aa0750d2982ea6767cd353b0%22',
    '__stripe_mid': '93df8f3f-cf6f-4ccd-9e78-231021ca231f76abc7',
    'sb-btsplwsgjvpilxywmaba-auth-token': '%5B%22eyJhbGciOiJIUzI1NiIsImtpZCI6IjkvdHdyWllvN1ZsOFZ6czEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J0c3Bsd3NnanZwaWx4eXdtYWJhLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI1ODU2ZmZkYy0zYWQyLTRmMTQtOGI0MS04ZDdmZWIwMGM4ZjIiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM0NDA2NzYzLCJpYXQiOjE3MzQ0MDMxNjMsImVtYWlsIjoibm5kZG9vbm5uZGRvb25AZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6Im5uZGRvb25ubmRkb29uQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiI1ODU2ZmZkYy0zYWQyLTRmMTQtOGI0MS04ZDdmZWIwMGM4ZjIifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTczMzE5NTU4NX1dLCJzZXNzaW9uX2lkIjoiYzc5MzdmMjMtMDc3Yi00Mzg0LWE3NTAtNWI4OGU5NmU3Nzk0IiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.LTb9Ak6Wjlm_GpvMpkVqeOpc7d7AgzJ3I93f6taC_tA%22%2C%22B8X5qVHXw6A0sRvpp-5j4Q%22%2Cnull%2Cnull%2Cnull%5D'
}

BASE_URL = "https://app.euka.ai/api/content-analysis"

@router.get("/", summary="獲取分類列表")
async def get_categories() -> CategoryListResponse:
    """
    獲取所有分類列表
    """
    response = requests.get(
        f"{BASE_URL}/categories",
        cookies=COOKIES,
        headers=HEADERS
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch categories"
        )
        
    return response.json()

@router.get("/{category_id}", summary="獲取特定分類詳情")
async def get_category_details(category_id: int) -> CategoryDetailResponse:
    """
    通過分類ID獲取特定分類的詳細信息
    """
    response = requests.get(
        f"{BASE_URL}/categories/{category_id}",
        cookies=COOKIES,
        headers=HEADERS
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Category with id {category_id} not found"
        )
        
    return response.json()

@router.get("/{category_id}/brands", summary="獲取分類相關品牌")
async def get_category_brands(
    category_id: int,
    page: int = 1,
    page_size: int = 10
) -> CategoryBrandsResponse:
    """
    獲取特定分類下的品牌列表
    """
    params = {
        'category-id': str(category_id),
        'page': page,
        'pageSize': page_size
    }
    
    response = requests.get(
        f"{BASE_URL}/brands",
        params=params,
        cookies=COOKIES,
        headers=HEADERS
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to fetch brands for category {category_id}"
        )
        
    return response.json() 