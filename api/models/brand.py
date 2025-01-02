from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class BrandListItem(BaseModel):
    seller_id: str
    name: str
    num_products: int
    created_at: datetime
    total_sales: int
    category_id: int
    hashtags_search_term: Optional[str] = None
    last_updated_at: datetime
    social_listening_analysis_json: Optional[Any] = None
    brand_url: Optional[str] = None

class BrandListResponse(BaseModel):
    data: List[BrandListItem]
    total: int

class BrandDetailResponse(BrandListItem):
    pass

class BrandAnalytics(BaseModel):
    follower_ages: Dict[str, str]
    follower_genders: Dict[str, str]
    follower_locations: Dict[str, str]
    creator_genders: Dict[str, str]
    creator_languages: Dict[str, str]

class BrandAnalyticsResponse(BaseModel):
    data: BrandAnalytics 