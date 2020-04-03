<template>
<div class="p-3">
  <div class="container bg-white rounded-lg mx-auto p-3">
    <div class="flex justify-between">
      <h1 class="text-2xl lg:text-4xl font-medium">Overview</h1>
      <a v-on:click="createSettings" class="self-center cursor-pointer bg-green-500 hover:bg-green-600 focus:outline-none rounded text-white text-sm font-medium tracking-wide p-2">New settings</a>
    </div>
    <ul>
      <li v-for="item, index in results" v-bind:key="index" class="bg-gray-200 rounded mt-3 p-2">
        <div class="lg:flex justify-between">
          <div class="lg:w-2/6 mb-2 lg:mb-0">
            <h3 class="font-bold">Recipient</h3>
            <p>{{ item.recipient }}</p>
          </div>
          <div class="lg:w-2/6 mb-2 lg:mb-0">
            <h3 class="font-bold">SMTP Server</h3>
            <p>{{ item.smtp_server }}</p>
          </div>
          <div class="lg:w-1/6 mb-2 lg:mb-0">
            <h3 class="font-bold">SMTP Port</h3>
            <p>{{ item.smtp_port }}</p>
          </div>
          <div class="lg:w-1/6 mb-2 lg:mb-0">
            <p class="lg:text-right lg:mt-4">
              <nuxt-link v-bind:to="generateLink(item.id)" class="bg-blue-500 hover:bg-blue-600 focus:outline-none rounded text-white text-sm font-medium tracking-wide p-2 mr-1">Edit</nuxt-link>
              <a v-on:click="deleteSettings(item.id, index)" class="cursor-pointer bg-red-500 hover:bg-red-600 focus:outline-none rounded text-white text-sm font-medium tracking-wide p-2">Delete</a>
            </p>
          </div>
        </div>
      </li>
    </ul>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      results: []
    }
  },
  created() {
    this.$axios.$get(process.env.API_URL + '/api/v1/settings/u/' + this.userId).then(res => {
      this.results = res
    }).catch(error => {
      if (error.hasOwnProperty('response')) {
        console.log(error.response.data)
      } else {
        console.log(error.message)
      }
    })
  },
  computed: {
    userId() {
      return this.$store.state.userId
    }
  },
  middleware: 'auth',
  methods: {
    generateLink(id) {
      return '/account/settings/' + id
    },
    createSettings() {
      this.$axios.$post(process.env.API_URL + '/api/v1/settings/u/' + this.userId).then(res => {
        this.$router.push({
          name: 'account-settings-id',
          params: {
            id: res.id
          }
        })
      }).catch(error => {
        if (error.hasOwnProperty('response')) {
          console.log(error.response.data)
        } else {
          console.log(error.message)
        }
      })
    },
    deleteSettings(settingsId, index) {
      this.$axios.$delete(process.env.API_URL + '/api/v1/settings/i/' + settingsId).then(res => {
        this.results.splice(index)
      }).catch(error => {
        if (error.hasOwnProperty('response')) {
          console.log(error.response.data)
        } else {
          console.log(error.message)
        }
      })
    }
  }
}
</script>
