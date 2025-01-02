from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union, Any
from datetime import datetime

class HookExample(BaseModel):
    video_id: str
    hook_phrasing: str

class Hook(BaseModel):
    examples: List[HookExample]
    hook_name: str

class HooksData(BaseModel):
    data: List[HookExample]

class SellingPointExample(BaseModel):
    video_id: str
    selling_point_phrasing: str

class SellingPoint(BaseModel):
    examples: List[SellingPointExample]
    selling_point: str

class VideoFormatExample(BaseModel):
    video_id: str
    explanation: str

class VideoFormat(BaseModel):
    examples: List[VideoFormatExample]
    description: str
    tips_to_use: str
    video_format_name: str

class ProductListItem(BaseModel):
    product_id: str
    seller_id: str
    title: str
    sold_count: int
    shipping_fee: Optional[float] = None
    original_price: Optional[float] = None
    real_price: float
    created_at: datetime
    category_id: int
    hooks_analysis_json: Optional[Any] = None
    selling_points_analysis_json: Optional[Any] = None
    video_formats_analysis_json: Optional[Any] = None
    last_analysis_at: Optional[datetime] = None
    last_updated_at: Optional[datetime] = None

class ProductListResponse(BaseModel):
    data: List[ProductListItem]
    total: int

# 保留詳情相關的模型，但根據需要調整
class ProductSeller(BaseModel):
    name: str
    seller_id: str
    seller_photo_url: Optional[str] = None

class ProductCreator(BaseModel):
    handle: str
    email: Optional[str] = None
    follower_count: Optional[str] = None
    creator_profile_url: Optional[str] = None

class ProductDetailBase(BaseModel):
    title: str
    hooks_analysis_json: Optional[Any] = None
    selling_points_analysis_json: Optional[Any] = None
    video_formats_analysis_json: Optional[Any] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    category: Optional[str] = None
    photo_url: Optional[str] = None
    total_sales: Optional[int] = None
    total_revenue: Optional[float] = None
    total_views: Optional[int] = None
    total_likes: Optional[int] = None

class ProductDetail(ProductDetailBase):
    pass

class ProductDetailResponse(BaseModel):
    title: str
    hooks_analysis_json: Optional[Any] = None
    selling_points_analysis_json: Optional[Any] = None
    video_formats_analysis_json: Optional[Any] = None
    # ... ���他可能的字段 ...

class DemographicsData(BaseModel):
    follower_ages: Dict[str, str]
    follower_genders: Dict[str, str]
    creator_genders: Dict[str, str]
    creator_languages: Dict[str, str]
    follower_locations: Dict[str, str]

class ProductAnalyticsResponse(BaseModel):
    data: DemographicsData 