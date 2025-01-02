// src/models/InfluencerFilter.js
export class InfluencerFilter {
    constructor({
      query = '',
      page = 1,
      perPage = 10,
      emailNotNull = false,
      targetCategories = [],
      targetFollowerCounts = [],
      targetGMVs = [],
      targetGender = null,
      targetLanguages = []
    }) {
      this.query = query;
      this.page = page;
      this.perPage = perPage;
      this.emailNotNull = emailNotNull;
      this.targetCategories = targetCategories;
      this.targetFollowerCounts = targetFollowerCounts;
      this.targetGMVs = targetGMVs;
      this.targetGender = targetGender;
      this.targetLanguages = targetLanguages;
    }
  
    asRequestParams() {
        return {
          query: this.query,
          page: this.page,
          perPage: this.perPage,
          emailNotNull: this.emailNotNull,
          targetCategories: this.targetCategories,
          targetFollowerCounts: this.targetFollowerCounts,
          targetGmvs: this.targetGMVs,
          targetGender: this.targetGender,
          targetLanguages: this.targetLanguages
        };
      }
      
  }