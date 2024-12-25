<template>
  <div class="mb-8">
    <h2 class="text-2xl font-bold mb-8">Audience Demographics</h2>
    <div class="grid grid-cols-3 gap-8">
      <div class="text-center">
        <h3 class="text-lg font-semibold mb-6">Gender</h3>
        <div class="bg-white p-4 rounded-lg shadow h-[250px]">
          <Doughnut :data="genderData" :options="chartOptions" />
        </div>
      </div>
      <div class="text-center">
        <h3 class="text-lg font-semibold mb-6">Age</h3>
        <div class="bg-white p-4 rounded-lg shadow h-[250px]">
          <Doughnut :data="ageData" :options="chartOptions" />
        </div>
      </div>
      <div class="text-center">
        <h3 class="text-lg font-semibold mb-6">Top 5 Locations</h3>
        <div class="bg-white p-4 rounded-lg shadow h-[250px]">
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
          data: [this.data.gender.female, this.data.gender.male],
          backgroundColor: ['#FF85C0', '#5B8FF9']
        }]
      }
    },
    ageData() {
      return {
        labels: ['18-24', '25-34', '35-44', '45-54', '55+'],
        datasets: [{
          data: [
            this.data.age['18-24'],
            this.data.age['25-34'],
            this.data.age['35-44'],
            this.data.age['45-54'],
            this.data.age['55+']
          ],
          backgroundColor: ['#5B8FF9', '#FFD666', '#5AD8A6', '#8B7CE1', '#FF9F7F']
        }]
      }
    },
    locationData() {
      return {
        labels: this.data.locations.map(loc => loc.name),
        datasets: [{
          data: this.data.locations.map(loc => loc.value),
          backgroundColor: new Array(5).fill({
            type: 'linear',
            x: 0,
            y: 0,
            x2: 1,
            y2: 0,
            colorStops: [{
              offset: 0,
              color: '#1890FF'
            }, {
              offset: 1,
              color: '#36CBCB'
            }]
          })
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
              label: (context) => `${context.raw}%`
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
              color: '#666',
              callback: (value) => `${value}%`
            }
          },
          y: {
            grid: {
              display: false
            },
            ticks: {
              color: '#666'
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