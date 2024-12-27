<template>
  <div class="grid grid-cols-2 gap-6">
    <!-- Gender Distribution -->
    <div class="p-4 rounded-lg bg-[#F8F9FA]">
      <h3 class="text-lg font-medium text-center mb-2">Gender</h3>
      <div class="h-[180px]">
        <Doughnut 
          v-if="genderChartData"
          :data="genderChartData"
          :options="genderChartOptions"
        />
      </div>
    </div>

    <!-- Language Distribution -->
    <div class="p-4 rounded-lg bg-[#F8F9FA]">
      <h3 class="text-lg font-medium text-center mb-2">Language</h3>
      <div class="h-[180px]">
        <Doughnut 
          v-if="languageChartData"
          :data="languageChartData"
          :options="languageChartOptions"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

export default {
  name: 'CreatorDemographics',
  components: {
    Doughnut
  },
  props: {
    genderData: {
      type: Object,
      required: true
    },
    languageData: {
      type: Object,
      required: true
    }
  },
  computed: {
    genderChartData() {
      return {
        labels: ['Female', 'Male'],
        datasets: [{
          data: [this.genderData.female, this.genderData.male],
          backgroundColor: ['#FF6384', '#36A2EB'],
          hoverBackgroundColor: ['#FF6384', '#36A2EB']
        }]
      }
    },
    genderChartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '60%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 12,
              padding: 15,
              font: {
                size: 12
              }
            }
          }
        }
      }
    },
    languageChartData() {
      const sortedLanguages = Object.entries(this.languageData)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
      
      return {
        labels: sortedLanguages.map(([lang]) => lang.toUpperCase()),
        datasets: [{
          data: sortedLanguages.map(([, value]) => value),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
          hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        }]
      }
    },
    languageChartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '60%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 12,
              padding: 15,
              font: {
                size: 12
              }
            }
          }
        }
      }
    }
  }
}
</script> 