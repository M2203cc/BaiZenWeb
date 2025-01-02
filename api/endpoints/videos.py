from fastapi import APIRouter, HTTPException
from typing import List, Optional
from api.models.video import (
    VideoDetail, 
    VideoListResponse, 
    VideoDetailResponse, 
    DemographicsResponse
)
import requests
from datetime import datetime

router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
    responses={404: {"description": "Video not found"}}
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
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

COOKIES = {
    'sb-btsplwsgjvpilxywmaba-auth-token-code-verifier': '%22e8dcaf23493502d311a3eba0603082a93b5f1f8dd9e5591d317e538ec9bfc72f91249d752196e6d77cf1f329aa0750d2982ea6767cd353b0%22',
    '__stripe_mid': '93df8f3f-cf6f-4ccd-9e78-231021ca231f76abc7',
    'sb-btsplwsgjvpilxywmaba-auth-token': '%5B%22eyJhbGciOiJIUzI1NiIsImtpZCI6IjkvdHdyWllvN1ZsOFZ6czEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J0c3Bsd3NnanZwaWx4eXdtYWJhLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI1ODU2ZmZkYy0zYWQyLTRmMTQtOGI0MS04ZDdmZWIwMGM4ZjIiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM0NDA2NzYzLCJpYXQiOjE3MzQ0MDMxNjMsImVtYWlsIjoibm5kZG9vbm5uZGRvb25AZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6Im5uZGRvb25ubmRkb29uQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiI1ODU2ZmZkYy0zYWQyLTRmMTQtOGI0MS04ZDdmZWIwMGM4ZjIifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTczMzE5NTU4NX1dLCJzZXNzaW9uX2lkIjoiYzc5MzdmMjMtMDc3Yi00Mzg0LWE3NTAtNWI4OGU5NmU3Nzk0IiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.LTb9Ak6Wjlm_GpvMpkVqeOpc7d7AgzJ3I93f6taC_tA%22%2C%22B8X5qVHXw6A0sRvpp-5j4Q%22%2Cnull%2Cnull%2Cnull%5D'
}

BASE_URL = "https://app.euka.ai/api/content-analysis"

@router.get("/by-date", summary="根據時間區間獲取視頻列表")
async def get_videos_by_date(
    page: int = 1,
    page_size: int = 10,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    search: str = ""
) -> VideoListResponse:
    """
    根據時間區間獲取視頻列表
    """
    params = {
        'page': page,
        'pageSize': page_size,
        'search': search
    }
    
    if start_date:
        params['start-date'] = start_date.isoformat() + '.000Z'
    if end_date:
        params['end-date'] = end_date.isoformat() + '.999Z'
    
    response = requests.get(
        f"{BASE_URL}/videos",
        params=params,
        cookies=COOKIES,
        headers=HEADERS
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch videos by date range"
        )
    
    data = response.json()
    # 確保響應包含 total 字段
    if 'total' not in data:
        data['total'] = len(data.get('data', []))
        
    return data

@router.get("/", summary="獲取視頻列表")
async def get_videos(
    page: int = 1,
    page_size: int = 10,
    search: str = ""
) -> VideoListResponse:
    """
    獲取視頻列表，支持分頁和搜索
    """
    params = {
        'page': page,
        'pageSize': page_size,
        'search': search,
    }
    
    response = requests.get(
        f"{BASE_URL}/videos",
        params=params,
        cookies=COOKIES,
        headers=HEADERS
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch videos"
        )
    
    data = response.json()
    # 確保響應包含 total 字段
    if 'total' not in data:
        data['total'] = len(data.get('data', []))
        
    return data

@router.get("/{video_id}", summary="獲取特定視頻詳情")
async def get_video_details(video_id: str) -> VideoDetailResponse:
    """
    通過視頻ID獲取特定視頻的詳細信息
    """
    response = requests.get(
        f"{BASE_URL}/videos/{video_id}",
        cookies=COOKIES,
        headers=HEADERS
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Video with id {video_id} not found"
        )
        
    return response.json()

@router.get("/{video_id}/demographics", summary="獲取視頻人口統計數據")
async def get_video_demographics(video_id: str) -> DemographicsResponse:
    """
    獲取特定視頻的觀眾人口統計數據
    """
    params = {
        'video-ids': video_id
    }
    
    response = requests.get(
        f"{BASE_URL}/demographics",
        params=params,
        cookies=COOKIES,
        headers=HEADERS
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to fetch demographics for video {video_id}"
        )
        
    return response.json()