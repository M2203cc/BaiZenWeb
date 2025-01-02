from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class InfluencerFilter(BaseModel):
    query: str = ""
    page: int = 1
    per_page: int = 10
    email_not_null: bool = False
    target_categories: Optional[List[str]] = None
    target_follower_counts: Optional[List[str]] = None
    target_gmvs: Optional[List[str]] = None
    target_gender: Optional[str] = None
    target_languages: Optional[List[str]] = None

    class Config:
        alias_generator = lambda x: ''.join([x[0].lower() + x[1:] if i == 0 else x.capitalize() for i, x in enumerate(x.split('_'))])
        populate_by_name = True

    @property
    def as_request_params(self) -> dict:
        """將過濾條件轉換為API請求參數，只包含非None的參數"""
        params = {
            'query': self.query,
            'page': self.page,
            'perPage': self.per_page,
            'emailNotNull': self.email_not_null,
        }
        
        if self.target_categories is not None:
            params['targetCategories'] = self.target_categories
        if self.target_follower_counts is not None:
            params['targetFollowerCounts'] = self.target_follower_counts
        if self.target_gmvs is not None:
            params['targetGMVs'] = self.target_gmvs
        if self.target_gender is not None:
            params['targetGender'] = self.target_gender
        if self.target_languages is not None:
            params['targetLanguages'] = self.target_languages
            
        return params

class Creator(BaseModel):
    uid_shop: str
    handle: str
    bio: Optional[str] = ''  # 修改为可选字段，默认为空字符串
    product_category: List[str]
    follower_count: str
    gmv_30d: str
    gmv_30d_num: float
    email: Optional[str] = None
    avg_video_engagement_30d: str
    avatar_url: str

class InfluencerListResponse(BaseModel):
    creators: List[Creator]
    total_pages: int = Field(alias='totalPages')
    total_creators: int = Field(alias='totalCreators')

    class Config:
        populate_by_name = True 