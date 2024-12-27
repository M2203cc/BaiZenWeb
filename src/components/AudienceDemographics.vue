<template>
  <div class="grid grid-cols-3 gap-6">
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

    <!-- Age Distribution -->
    <div class="p-4 rounded-lg bg-[#F8F9FA]">
      <h3 class="text-lg font-medium text-center mb-2">Age</h3>
      <div class="h-[180px]">
        <Doughnut 
          v-if="ageChartData"
          :data="ageChartData"
          :options="ageChartOptions"
        />
      </div>
    </div>

    <!-- Top 5 Locations -->
    <div class="p-4 rounded-lg bg-[#F8F9FA]">
      <h3 class="text-lg font-medium text-center mb-2">Top 5 Locations</h3>
      <div class="h-[180px]">
        <Bar
          v-if="locationsChartData"
          :data="locationsChartData"
          :options="locationsChartOptions"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js'
import { Doughnut, Bar } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement)

export default {
  name: 'AudienceDemographics',
  components: {
    Doughnut,
    Bar
  },
  props: {
    genderData: {
      type: Object,
      required: true
    },
    ageData: {
      type: Object,
      required: true
    },
    locationsData: {
      type: Array,
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
    ageChartData() {
      const ageGroups = Object.entries(this.ageData)
      
      return {
        labels: ageGroups.map(([age]) => age),
        datasets: [{
          data: ageGroups.map(([, value]) => value),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
          hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        }]
      }
    },
    ageChartOptions() {
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
    locationsChartData() {
      return {
        labels: this.locationsData.map(loc => loc.name),
        datasets: [{
          data: this.locationsData.map(loc => loc.value),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
          borderRadius: 4
        }]
      }
    },
    locationsChartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          x: {
            grid: {
              display: true,
              color: '#f0f0f0'
            },
            ticks: {
              callback: value => `${value}%`,
              font: {
                size: 12
              }
            }
          },
          y: {
            grid: {
              display: false
            },
            ticks: {
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