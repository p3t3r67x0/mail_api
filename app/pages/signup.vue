<template>
<div class="flex items-center justify-center mt-3 mx-3 lg:mx-0 lg:mt-32">
  <form @submit.prevent="signupSubmit" class="bg-white rounded-lg w-full max-w-sm p-3">
    <h1 class="text-2xl lg:text-4xl font-medium mb-3">Signup</h1>
    <p v-if="showResponse" v-bind:class="classResponse" class="lg:text-lg mb-3">{{ response }}</p>
    <div class="w-full mb-6">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="name">
        Name
      </label>
      <input name="name" v-model="name" v-bind:class="{'border-red-500': errors.name}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        id="name" type="text" placeholder="Jane Doe">
      <p v-if="errors.name" class="text-red-500 text-xs italic">Please enter your name.</p>
    </div>
    <div class="w-full mb-6">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="email">
        Email
      </label>
      <input name="email" v-model="email" v-bind:class="{'border-red-500': errors.email}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        id="email" type="text" placeholder="me@example.com">
      <p v-if="errors.email" class="text-red-500 text-xs italic">Please enter a valid email.</p>
    </div>
    <div class="w-full mb-6">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="password">
        Password
      </label>
      <input name="password" v-model="password" v-bind:class="{'border-red-500': errors.password}" class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white" id="password"
        type="password" placeholder="••••••••">
      <p v-if="errors.password" class="text-red-500 text-xs italic">Please fill out this field.</p>
    </div>
    <p class="text-right">
      <button class="cursor-pointer bg-blue-500 hover:bg-blue-600 focus:outline-none rounded text-white text-sm font-medium tracking-wide p-2" type="submit">Login</button>
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
        name: false,
        email: false,
        password: false
      },
      name: null,
      email: null,
      password: null,
      response: null,
      showResponse: false,
      classResponse: null,
      emailRegex: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    }
  },
  watch: {
    name: function() {
      if (this.name.trim() !== '') {
        if (this.name.trim().length > 2) {
          this.errors.name = false
        } else {
          this.errors.name = true
        }
      }
    },
    email: function() {
      if (this.email.trim() !== '') {
        if (this.emailRegex.test(this.email.trim())) {
          this.errors.email = false
        } else {
          this.errors.email = true
        }
      }
    },
    password: function() {
      if (this.password.trim() !== '') {
        if (this.password.trim().length > 2) {
          this.errors.password = false
        } else {
          this.errors.password = true
        }
      }
    }
  },
  middleware: 'auth',
  methods: {
    signupSubmit() {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.name) {
        this.errors.name = true
      }

      if (!this.email) {
        this.errors.email = true
      }

      if (!this.password) {
        this.errors.password = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios.$post(process.env.API_URL + '/api/v1/signup', {
          'name': this.name.trim(),
          'email': this.email.trim(),
          'password': this.password.trim()
        }).then(res => {
          console.log(res)
          this.classResponse = 'text-green-500'
          this.showResponse = true
          this.response = res.message
        }).catch(error => {
          this.classResponse = 'text-red-500'
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
