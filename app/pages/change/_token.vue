<template>
<div class="flex items-center justify-center mt-3 mx-3 lg:mx-0 lg:mt-32">
  <form @submit.prevent="changePasswordSubmit" class="bg-white rounded-lg w-full max-w-sm p-3">
    <h1 class="text-2xl lg:text-4xl font-medium mb-3">Change password</h1>
    <p v-if="showResponse" class="text-red-500 lg:text-lg mb-3">{{ response }}</p>
    <div class="w-full mb-6">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="password">
        New password
      </label>
      <input name="password" v-model="password" v-bind:class="{'border-red-500': errors.password}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        id="password" type="password" placeholder="password">
      <p v-if="errors.password" class="text-red-500 text-xs italic">Please enter a valid password.</p>
    </div>
    <div class="w-full mb-6">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="confirmPassword">
        Confirm password
      </label>
      <input name="confirmPassword" v-model="confirmPassword" v-bind:class="{'border-red-500': errors.confirmPassword}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        id="confirmPassword" type="password" placeholder="password">
      <p v-if="errors.confirmPassword" class="text-red-500 text-xs italic">Please enter a valid password.</p>
    </div>
    <p class="text-right">
      <nuxt-link to="/reset" class="text-blue-400 hover:text-blue-600 focus:outline-none mr-2">Forgot password</nuxt-link>
      <button class="cursor-pointer bg-blue-500 hover:bg-blue-600 focus:outline-none rounded text-white text-sm font-medium tracking-wide p-2" type="submit">Save password</button>
    </p>
  </form>
</div>
</template>

<script>
const Cookie = require('js-cookie')

export default {
  data() {
    return {
      errors: {
        password: false,
        confirmPassword: false
      },
      password: null,
      confirmPassword: null,
      showResponse: false,
      response: null
    }
  },
  watch: {
    password: function() {
      if (this.password.trim() !== '') {
        if (this.password.trim().length > 7) {
          this.errors.password = false
        } else {
          this.errors.password = true
        }
      }
    },
    confirmPassword: function() {
      if (this.confirmPassword.trim() !== '') {
        if (this.confirmPassword.trim() === this.password.trim()) {
          this.errors.confirmPassword = false
        } else {
          this.errors.confirmPassword = true
        }
      }
    }
  },
  computed: {
    token() {
      return this.$route.params.token
    }
  },
  middleware: 'auth',
  methods: {
    changePasswordSubmit() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.password) {
        this.errors.password = true
      }

      if (!this.confirmPassword) {
        this.errors.confirmPassword = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios.$put(process.env.API_URL + '/api/v1/change', {
          'token': this.token.trim(),
          'password': this.password.trim()
        }).then(res => {
          console.log(res)
          this.$router.push({
            name: 'login'
          })
        }).catch(error => {
          this.showResponse = true

          if (error.hasOwnProperty('response')) {
            this.response = error.response.data.message
          } else {
            this.response = error.message
          }
        })
      }
    }
  }
}
</script>
