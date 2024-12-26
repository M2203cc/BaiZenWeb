const brandAPI = {
  async getBrands({ page = 1, pageSize = 10, search = '', withImages = true } = {}) {
    try {
      const params = new URLSearchParams({
        page: String(page),
        page_size: String(pageSize),
        with_images: String(withImages)
      })
      
      if (search) {
        params.append('search', search)
      }

      const url = `http://192.168.0.170:8000/brands/?${params}`
      console.log('Fetching brands from:', url)

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'accept': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      console.log('Received data:', data)
      return {
        data: data.data,
        total: data.total || data.data.length
      }

    } catch (error) {
      console.error('Error fetching brands:', error)
      throw error
    }
  },

  async getBrandDetails(brandId) {
    try {
      const response = await fetch(`http://192.168.0.170:8000/brands/${brandId}`, {
        method: 'GET',
        headers: {
          'accept': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return response.json()
    } catch (error) {
      console.error('Error fetching brand details:', error)
      throw error
    }
  },

  async getBrandAnalytics(brandId, retries = 3) {
    const timeout = 30000; // 增加超时时间到30秒
    const retryDelay = 2000; // 重试间隔2秒

    for (let i = 0; i < retries; i++) {
      let controller;
      let timeoutId;

      try {
        controller = new AbortController();
        
        // 创建一个超时Promise
        const timeoutPromise = new Promise((_, reject) => {
          timeoutId = setTimeout(() => {
            controller.abort();
            reject(new Error('Request timeout'));
          }, timeout);
        });

        // 创建请求Promise
        const fetchPromise = fetch(
          `http://192.168.0.170:8000/brands/${brandId}/analytics`,
          {
            method: 'GET',
            headers: {
              'accept': 'application/json'
            },
            signal: controller.signal
          }
        );

        // 使用 Promise.race 来处理超时
        const response = await Promise.race([fetchPromise, timeoutPromise]);

        // 清除超时定时器
        clearTimeout(timeoutId);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;

      } catch (error) {
        // 清除超时定时器
        if (timeoutId) {
          clearTimeout(timeoutId);
        }

        console.warn(`Attempt ${i + 1} failed:`, error.message);
        
        if (i === retries - 1) {
          // 如果是最后一次尝试，抛出错误
          throw new Error(`Failed to fetch analytics after ${retries} attempts: ${error.message}`);
        }
        
        // 等待一段时间后重试
        await new Promise(resolve => setTimeout(resolve, retryDelay));
      }
    }
  },

  async getBrandProducts(brandId, page = 1, pageSize = 7) {
    try {
      const params = new URLSearchParams({
        page: String(page),
        page_size: String(pageSize)
      });

      const response = await fetch(
        `http://192.168.0.170:8000/brands/${brandId}/products?${params}`,
        {
          method: 'GET',
          headers: {
            'accept': 'application/json'
          }
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        data: data.data,
        total: data.total
      };
    } catch (error) {
      console.error('Error fetching brand products:', error);
      throw error;
    }
  },

  async getBrandVideos(brandId, page = 1, pageSize = 10) {
    try {
      const params = new URLSearchParams({
        page: String(page),
        page_size: String(pageSize)
      });

      const response = await fetch(
        `http://192.168.0.170:8000/brands/${brandId}/videos?${params}`,
        {
          method: 'GET',
          headers: {
            'accept': 'application/json'
          }
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        data: data.data,
        total: data.total
      };
    } catch (error) {
      console.error('Error fetching brand videos:', error);
      throw error;
    }
  }
}

export default brandAPI 