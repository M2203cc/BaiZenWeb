from pydantic import BaseModel
from typing import List, Optional, Dict

class VideoAnalysis(BaseModel):
    hooks: List[str]
    key_idea: str
    transcript: str
    call_to_action: str
    selling_points: List[str]

class VideoSeller(BaseModel):
    name: str
    seller_id: Optional[str] = None

class VideoProduct(BaseModel):
    title: str
    sellers: VideoSeller
    seller_id: str
    product_id: str

class VideoCreatorList(BaseModel):
    email: Optional[str] = None
    handle: str
    uid_shop: str
    hashtags: Optional[List[str]] = []
    follower_count: Optional[str] = None

class VideoCreatorDetail(BaseModel):
    handle: str
    hashtags: Optional[List[str]] = []
    follower_count: Optional[str] = None

class VideoDetailBase(BaseModel):
    video_id: str
    posted_date: str
    views_count: int
    likes_count: int
    description: Optional[str] = None
    photo_downloaded: Optional[bool] = None
    social_listening_term: Optional[str] = None
    revenue: Optional[float] = None
    analysis_json: Optional[VideoAnalysis] = None
    social_listening_analysis_json: Optional[dict] = None
    seller_products: VideoProduct
    thumbnail_url: str
    creator_profile_url: Optional[str] = None
    seller_product_photo_url: Optional[str] = None
    seller_photo_url: Optional[str] = None

class VideoDetail(VideoDetailBase):
    creators: VideoCreatorList

class VideoDetailSingle(VideoDetailBase):
    creators: VideoCreatorDetail

class VideoDetailResponse(BaseModel):
    data: VideoDetailSingle

class VideoListResponse(BaseModel):
    message: str
    data: List[VideoDetail]
    total: int

class DemographicsData(BaseModel):
    follower_ages: Dict[str, str]
    follower_genders: Dict[str, str]
    creator_genders: Dict[str, str]
    creator_languages: Dict[str, str]
    follower_locations: Dict[str, str]

class DemographicsResponse(BaseModel):
    data: DemographicsData