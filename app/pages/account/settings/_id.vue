<template>
<div class="p-3">
  <div class="container bg-white rounded-lg mx-auto p-3">
    <h1 class="text-2xl lg:text-4xl font-medium mb-2">Settings</h1>
    <p v-if="showResponse" class="text-green-500 lg:text-lg mb-3">{{ response }}</p>
    <form ref="contactForm" @submit="submitForm" class="w-full">
      <div class="flex flex-wrap -mx-3 mb-3">
        <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="first-name">
            First Name
          </label>
          <input name="first-name" v-model="settings.first_name" v-bind:class="{'border-red-500': errors.first_name}" class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white"
            id="first-name" type="text" placeholder="Jane">
          <p v-if="errors.first_name" class="text-red-500 text-xs italic">Please fill out this field.</p>
        </div>
        <div class="w-full md:w-1/2 px-3">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="last-name">
            Last Name
          </label>
          <input name="last-name" v-model="settings.last_name" v-bind:class="{'border-red-500': errors.last_name}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="last-name" type="text" placeholder="Doe">
          <p v-if="errors.last_name" class="text-red-500 text-xs italic">Please fill out this field.</p>
        </div>
      </div>
      <div class="flex flex-wrap -mx-3 mb-6">
        <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="username">
            Username
          </label>
          <input name="username" v-model="settings.username" v-bind:class="{'border-red-500': errors.username}" class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white" id="username"
            type="text" placeholder="Jane">
          <p v-if="errors.username" class="text-red-500 text-xs italic">Please fill out this field.</p>
        </div>
        <div class="w-full md:w-1/2 px-3">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="password">
            Password
          </label>
          <input name="password" v-model="settings.password" v-bind:class="{'border-red-500': errors.password}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="password" type="text" placeholder="Doe">
          <p v-if="errors.password" class="text-red-500 text-xs italic">Please fill out this field.</p>
        </div>
      </div>
      <div class="flex flex-wrap -mx-3 mb-6">
        <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="recipient">
            Recipient
          </label>
          <input name="recipient" v-model="settings.recipient" v-bind:class="{'border-red-500': errors.recipient}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="recipient" type="text">
          <p v-if="errors.recipient" class="text-red-500 text-xs italic">Please enter a valid recipient address.</p>
        </div>
        <div class="w-full md:w-1/2 px-3">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="secret">
            Secret
          </label>
          <input name="secret" v-model="settings.secret" v-bind:class="{'border-red-500': errors.secret}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="secret" type="text">
          <p v-if="errors.secret" class="text-red-500 text-xs italic">Please fill out this field.</p>
        </div>
      </div>
      <div class="flex flex-wrap -mx-3 mb-6">
        <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="smtp_port">
            SMTP Port
          </label>
          <input name="smtp_port" v-model="settings.smtp_port" v-bind:class="{'border-red-500': errors.smtp_port}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="smtp_port" type="text">
          <p v-if="errors.smtp_port" class="text-red-500 text-xs italic">Please fill out this field.</p>
        </div>
        <div class="w-full md:w-1/2 px-3">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="smtp">
            SMTP Server
          </label>
          <input name="smtp" v-model="settings.smtp_server" v-bind:class="{'border-red-500': errors.smtp_server}" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="smtp" type="text">
          <p v-if="errors.smtp_server" class="text-red-500 text-xs italic">Please fill out this field.</p>
        </div>
      </div>
      <div class="flex flex-wrap -mx-3 mb-6">
        <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="use_ssl">
            Use SSL
          </label>
          <div class="relative">
            <select name="use_ssl" v-model="settings.use_ssl" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="use_ssl">
              <option value="false" selected>False</option>
              <option value="true">True</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
              </svg>
            </div>
          </div>
        </div>
        <div class="w-full md:w-1/2 px-3 md:mb-0">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="use_tls">
            Use TLS
          </label>
          <div class="relative">
            <select name="use_tls" v-model="settings.use_tls" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded p-3 mb-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="use_tls">
              <option value="false">False</option>
              <option value="true">True</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
      <p class="text-right">
        <button class="bg-blue-500 hover:bg-blue-600 focus:outline-none rounded text-white text-sm font-medium tracking-wide p-2 mr-2" type="submit">
          Save
        </button>
        <nuxt-link to="/account/overview" class="bg-teal-500 hover:bg-teal-600 focus:outline-none rounded text-white text-sm font-medium tracking-wide p-2">
          Back
        </nuxt-link>
      </p>
    </form>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      response: '',
      showResponse: false,
      settings: {
        secret: '',
        username: '',
        password: '',
        smtp_port: '',
        smtp_server: '',
        recipient: '',
        first_name: '',
        last_name: '',
        use_ssl: false,
        use_tls: true
      },
      errors: {
        secret: false,
        username: false,
        password: false,
        smtp_port: false,
        smtp_server: false,
        recipient: false,
        first_name: false,
        last_name: false,
      },
      recipientRegex: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    }
  },
  computed: {
    settingsId() {
      return this.$route.params.id
    }
  },
  created() {
    this.$axios.$get('http://localhost:5000/api/v1/settings/i/' + this.settingsId).then(res => {
      this.settings = res
    }).catch(error => {
      console.log(error)
    })
  },
  watch: {
    'settings.first_name': function() {
      if (this.settings.first_name.trim() !== '') {
        if (this.settings.first_name.trim().length > 2) {
          this.errors.first_name = false
        } else {
          this.errors.first_name = true
        }
      }
    },
    'settings.last_name': function() {
      if (this.settings.last_name.trim() !== '') {
        if (this.settings.last_name.trim().length > 2) {
          this.errors.last_name = false
        } else {
          this.errors.last_name = true
        }
      }
    },
    'settings.recipient': function() {
      if (this.settings.recipient.trim() !== '') {
        if (this.recipientRegex.test(this.settings.recipient.trim())) {
          this.errors.recipient = false
        } else {
          this.errors.recipient = true
        }
      }
    },
    'settings.username': function() {
      if (this.settings.username.trim() !== '') {
        if (this.settings.username.trim().length > 2) {
          this.errors.username = false
        } else {
          this.errors.username = true
        }
      }
    },
    'settings.password': function() {
      if (this.settings.password.trim() !== '') {
        if (this.settings.password.trim().length > 2) {
          this.errors.password = false
        } else {
          this.errors.password = true
        }
      }
    },
    'settings.smtp_server': function() {
      if (this.settings.smtp_server.trim() !== '') {
        if (this.settings.smtp_server.trim().length > 2) {
          this.errors.smtp_server = false
        } else {
          this.errors.smtp_server = true
        }
      }
    },
    'settings.smtp_port': function() {
      if (this.settings.smtp_port.trim() !== '') {
        if (this.settings.smtp_port.trim().length > 2) {
          this.errors.smtp_port = false
        } else {
          this.errors.smtp_port = true
        }
      }
    },
    'settings.secret': function() {
      if (this.settings.secret.trim() !== '') {
        if (this.settings.secret.trim().length > 2) {
          this.errors.secret = false
        } else {
          this.errors.secret = true
        }
      }
    }
  },
  middleware: 'auth',
  methods: {
    submitForm: function(e) {
      const isValidForm = (currentValue) => currentValue !== true

      if (!this.settings.first_name) {
        this.errors.first_name = true
      }

      if (!this.settings.last_name) {
        this.errors.last_name = true
      }

      if (!this.settings.recipient) {
        this.errors.recipient = true
      }

      if (!this.settings.username) {
        this.errors.username = true
      }

      if (!this.settings.password) {
        this.errors.password = true
      }

      if (!this.settings.smtp_server) {
        this.errors.smtp_server = true
      }

      if (!this.settings.smtp_port) {
        this.errors.smtp_port = true
      }

      if (!this.settings.secret) {
        this.errors.secret = true
      }

      if (Object.values(this.errors).every(isValidForm) === true) {
        this.$axios.$put('http://localhost:5000/api/v1/settings/i/' + this.settingsId, {
          'use_ssl': this.settings.use_ssl,
          'use_tls': this.settings.use_tls,
          'secret': this.settings.secret.trim(),
          'username': this.settings.username.trim(),
          'password': this.settings.password.trim(),
          'recipient': this.settings.recipient.trim(),
          'first_name': this.settings.first_name.trim(),
          'last_name': this.settings.last_name.trim(),
          'smtp_server': this.settings.smtp_server.trim(),
          'smtp_port': this.settings.smtp_port.trim()
        }).then(res => {
          this.response = res.message
          this.showResponse = true
        }).catch(error => {
          console.log(error)
        })
      }

      e.preventDefault()
    }
  }
}
</script>
