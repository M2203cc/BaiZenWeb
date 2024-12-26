<template>
  <div class="mb-8">
    <h2 class="text-2xl font-bold mb-8">Creator Demographics</h2>
    <div class="grid grid-cols-2 gap-8">
      <div class="text-center">
        <h3 class="text-lg font-semibold mb-6">Gender</h3>
        <div class="bg-gray-50 p-4 rounded-lg h-[200px]">
          <Doughnut :data="genderData" :options="chartOptions" />
        </div>
      </div>
      <div class="text-center">
        <h3 class="text-lg font-semibold mb-6">Language</h3>
        <div class="bg-gray-50 p-4 rounded-lg h-[200px]">
          <Doughnut :data="languageData" :options="chartOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'
import { Doughnut } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

export default {
  name: 'CreatorDemographics',
  components: {
    Doughnut
  },
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  computed: {
    genderData() {
      return {
        labels: ['Female', 'Male'],
        datasets: [{
          data: [
            parseFloat(this.data.gender.female || 0),
            parseFloat(this.data.gender.male || 0)
          ],
          backgroundColor: ['#FF85C0', '#5B8FF9']
        }]
      }
    },
    languageData() {
      // 获取前5个主要语言
      const languages = {
        en: 'English',
        es: 'Spanish',
        fr: 'French',
        id: 'Indonesian',
        other: 'Other'
      }
      
      const mainLanguages = Object.entries(this.data.language)
        .map(([code, value]) => ({
          code,
          value: parseFloat(value || 0)
        }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 4)

      // 计算其他语言的总和
      const otherSum = Object.entries(this.data.language)
        .filter(([code]) => !mainLanguages.find(lang => lang.code === code))
        .reduce((sum, [, value]) => sum + parseFloat(value || 0), 0)

      // 准备图表数据
      const labels = [...mainLanguages.map(lang => languages[lang.code] || lang.code), 'Other']
      const values = [...mainLanguages.map(lang => lang.value), otherSum]

      return {
        labels,
        datasets: [{
          data: values,
          backgroundColor: ['#5B8FF9', '#FFD666', '#5AD8A6', '#8B7CE1', '#FF9F7F']
        }]
      }
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#666',
              usePointStyle: true,
              pointStyle: 'circle'
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => `${context.label}: ${context.raw.toFixed(1)}%`
            }
          }
        }
      }
    }
  }
}
</script>

<style scoped>
.v-chart {
  width: 100%;
  height: 100%;
  background-color: transparent !important;
}
</style> 