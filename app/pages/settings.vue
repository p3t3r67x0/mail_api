<template>
<div class="p-3">
  <div class="container bg-white rounded-lg mx-auto p-3">
    <h1 class="text-2xl lg:text-5xl font-medium mb-2">Settings</h1>
    <p v-if="showResponse" class="text-green-500 lg:text-lg mb-3">{{ response }}</p>
    <form ref="contactForm" @submit="submitForm" class="w-full">
      <div class="flex flex-wrap -mx-3 mb-6">
        <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="first-name">
            First Name
          </label>
          <input name="first-name" v-model="firstName" v-bind:class="{'border-red-500': errors.firstName}" class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white" id="first-name"
            type="text" placeholder="Jane">
          <p v-if="errors.firstName" class="text-red-500 text-xs italic">Please fill out this field.</p>
        </div>
        <div class="w-full md:w-1/2 px-3">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="last-name">
            Last Name
          </label>
          <input name="last-name" v-model="lastName" v-bind:class="{'border-red-500': errors.lastName}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="last-name" type="text" placeholder="Doe">
          <p v-if="errors.lastName" class="text-red-500 text-xs italic">Please fill out this field.</p>
        </div>
      </div>
      <div class="flex flex-wrap -mx-3 mb-6">
        <div class="w-full px-3">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="email">
            E-mail
          </label>
          <input name="email" v-model="email" v-bind:class="{'border-red-500': errors.email}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="email" type="text">
          <p v-if="errors.email" class="text-red-500 text-xs italic">Please enter a valid email address.</p>
        </div>
      </div>
      <div class="flex flex-wrap -mx-3 mb-6">
        <div class="w-full px-3">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="message">
            Message
          </label>
          <textarea name="message" v-model="message" v-bind:class="{'border-red-500': errors.message}" class="no-resize appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500 h-48 resize-none"
            id="message"></textarea>
          <p v-if="errors.message" class="text-red-500 text-xs italic">Please enter a minimum of three words.</p>
        </div>
      </div>
      <div class="md:flex md:items-center">
        <div class="md:w-1/3">
          <button class="bg-blue-400 hover:bg-blue-600 focus:outline-none text-white font-bold py-2 px-4 rounded" type="submit">
            Send
          </button>
        </div>
      </div>
    </form>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      showResponse: false,
      errors: {
        email: false,
        message: false,
        firstName: false,
        lastName: false,
      },
      email: '',
      message: '',
      firstName: '',
      lastName: '',
      honeypot: '',
      response: '',
      emailRegex: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    }
  },
  watch: {
    firstName: function() {
      if (this.firstName.trim() !== '') {
        if (this.firstName.trim().length > 2) {
          this.errors.firstName = false
        } else {
          this.errors.firstName = true
        }
      }
    },
    lastName: function() {
      if (this.lastName.trim() !== '') {
        if (this.lastName.trim().length > 2) {
          this.errors.lastName = false
        } else {
          this.errors.lastName = true
        }
      }
    },
    email: function() {
      if (this.email.trim() !== '') {
        if (this.email.trim().length > 2 && this.emailRegex.test(this.email.trim())) {
          this.errors.email = false
        } else {
          this.errors.email = true
        }
      }
    },
    message: function() {
      if (this.message.trim() !== '') {
        if (this.message.trim().length > 2) {
          this.errors.message = false
        } else {
          this.errors.message = true
        }
      }
    }
  },
  methods: {
    submitForm: function(e) {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.firstName) {
        this.errors.firstName = true
      }

      if (!this.lastName) {
        this.errors.lastName = true
      }

      if (!this.email) {
        this.errors.email = true
      }

      if (!this.message) {
        this.errors.message = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios.$post('/api/v1/settings', {
          "first_name": this.firstName.trim(),
          "last_name": this.lastName.trim(),
          "message": this.message.trim(),
          "email": this.email.trim()
        }).then(res => {
          console.log(res)
          this.response = res.message
          this.showResponse = true

          this.firstName = ''
          this.lastName = ''
          this.message = ''
          this.email = ''
        }).catch(error => {
          console.log(error)
        })
      }

      e.preventDefault()
    }
  }
}
</script>
