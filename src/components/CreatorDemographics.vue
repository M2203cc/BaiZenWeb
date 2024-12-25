<template>
  <div class="mb-8">
    <h2 class="text-2xl font-bold mb-8">Creator Demographics</h2>
    <div class="grid grid-cols-2 gap-8">
      <div class="text-center">
        <h3 class="text-lg font-semibold mb-6">Gender</h3>
        <div class="bg-white p-4 rounded-lg shadow h-[250px]">
          <Doughnut :data="genderData" :options="chartOptions" />
        </div>
      </div>
      <div class="text-center">
        <h3 class="text-lg font-semibold mb-6">Language</h3>
        <div class="bg-white p-4 rounded-lg shadow h-[250px]">
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
          data: [this.data.gender.female, this.data.gender.male],
          backgroundColor: ['#FF85C0', '#5B8FF9']
        }]
      }
    },
    languageData() {
      return {
        labels: ['English', 'French', 'Spanish', 'Other'],
        datasets: [{
          data: [
            this.data.language.english,
            this.data.language.french,
            this.data.language.spanish,
            this.data.language.other
          ],
          backgroundColor: ['#5B8FF9', '#FFD666', '#5AD8A6', '#8B7CE1']
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
              label: (context) => `${context.label}: ${context.raw}%`
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
  background-color: transparent;
}
</style> 