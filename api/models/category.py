from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class VideoExample(BaseModel):
    video_id: str
    explanation: str
    views_count: Optional[int] = None

class HookAnalysis(BaseModel):
    examples: List[VideoExample]
    hook_name: str
    tips_to_use: str
    description_of_technique: str

class SellingPointExample(BaseModel):
    video_id: str
    explanation: str
    views_count: Optional[int] = None

class SellingPoint(BaseModel):
    examples: List[SellingPointExample]
    description: str
    selling_point: str

class VideoFormatExample(BaseModel):
    video_id: str
    explanation: str

class VideoFormat(BaseModel):
    examples: List[VideoFormatExample]
    description: str
    tips_to_use: str
    why_it_works: str
    video_format_name: str

# 基礎分類模型，不包含可選字段
class CategoryBase(BaseModel):
    category_name: str
    hooks_analysis_json: List[HookAnalysis]
    selling_points_analysis_json: List[SellingPoint]
    video_formats_analysis_json: List[VideoFormat]

# 用於列表的分類模型，包含 id 和 num_products
class CategoryItem(CategoryBase):
    id: int
    num_products: List[Dict[str, int]]

class CategoryListResponse(BaseModel):
    data: List[CategoryItem]
    total: int

# 分類詳情直接使用基礎模型
class CategoryDetailResponse(CategoryBase):
    pass

class CategoryBrandsResponse(BaseModel):
    data: List[Any]
    total: int 