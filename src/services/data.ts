
interface Influencer {
    handle: string;          // TikTok 用户名
    email: string;          // 邮箱
    bio: string;            // 简介
    product_category: string[];   // 分类
    follower_count: string;      // 粉丝数
    gmv_30d: string;           // GMV
    dmv_30d_num?: number;     // 30天DMV数量
    avg_video_engagement_30d: string; // 30天平均视频互动
    avatar_url: string;        // 头像
  }  

interface SearchParams{
    // 搜索参数接口
    page: number;
    pagePage: number;
    query: string;
    targetCategories: string[];
    targetFollowerCounts: string[];
    targetGMVs: string[];
    targetLanguages: string[];
    targetGender: string;
    emailNotNull: boolean;
}