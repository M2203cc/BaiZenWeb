const brandAPI = {
  async getBrands({ page = 1, pageSize = 10, search = '' } = {}) {
    try {
      const params = new URLSearchParams({
        page: String(page),
        pageSize: String(pageSize)
      })
      
      if (search) {
        params.append('search', search)
      }

      const url = `/api/content-analysis/brands?${params}`
      console.log('Fetching brands from:', url)

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'accept': '*/*',
          'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
          'dnt': '1',
          'referer': 'https://app.euka.ai/content-analysis/brands',
          'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        },
        credentials: 'include'
      })

      console.log('Response status:', response.status)
      const data = await response.json()
      console.log('Received data:', data)
      return data

    } catch (error) {
      console.error('Error fetching brands:', error)
      throw error
    }
  },

  async getBrandDetails(brandId) {
    try {
      const response = await fetch(`/api/content-analysis/brands/${brandId}`, {
        method: 'GET',
        headers: {
          'accept': '*/*',
          'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
          'dnt': '1',
          'referer': 'https://app.euka.ai/content-analysis/brands',
          'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        },
        credentials: 'include'
      })

      return response.json()
    } catch (error) {
      console.error('Error fetching brand details:', error)
      throw error
    }
  }
}

export default brandAPI 