<template>
  <div class="mb-8">
    <h2 class="text-2xl font-bold mb-8">Audience Demographics</h2>
    <div class="grid grid-cols-3 gap-8">
      <div class="text-center">
        <h3 class="text-lg font-semibold mb-6">Gender</h3>
        <div class="bg-gray-50 p-4 rounded-lg h-[200px]">
          <Doughnut :data="genderData" :options="chartOptions" />
        </div>
      </div>
      <div class="text-center">
        <h3 class="text-lg font-semibold mb-6">Age</h3>
        <div class="bg-gray-50 p-4 rounded-lg h-[200px]">
          <Doughnut :data="ageData" :options="chartOptions" />
        </div>
      </div>
      <div class="text-center">
        <h3 class="text-lg font-semibold mb-6">Top 5 Locations</h3>
        <div class="bg-gray-50 p-4 rounded-lg h-[200px]">
          <Bar :data="locationData" :options="barOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar, Doughnut } from 'vue-chartjs'

ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
)

export default {
  name: 'AudienceDemographics',
  components: {
    Bar,
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
    ageData() {
      const ageRanges = ['18-24', '25-34', '35-44', '45-54', '55+']
      return {
        labels: ageRanges,
        datasets: [{
          data: ageRanges.map(range => parseFloat(this.data.age[range] || 0)),
          backgroundColor: ['#5B8FF9', '#FFD666', '#5AD8A6', '#8B7CE1', '#FF9F7F']
        }]
      }
    },
    locationData() {
      const locations = this.data.locations
        .map(loc => ({
          name: loc.name.split(' ')[0], // 只显示第一个单词
          value: parseFloat(loc.value)
        }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 5)

      return {
        labels: locations.map(loc => loc.name),
        datasets: [{
          data: locations.map(loc => loc.value),
          backgroundColor: '#1890FF'
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
    },
    barOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: (context) => `${context.raw.toFixed(1)}%`
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            grid: {
              display: false
            },
            ticks: {
              callback: (value) => `${value}%`
            }
          },
          y: {
            grid: {
              display: false
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