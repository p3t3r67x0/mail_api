<template>
<div v-click-outside="hideNav" class="fixed w-full bg-gray-900 mb-3 lg:mb-8">
  <div class="container mx-auto">
    <header class="flex flex-wrap items-center">
      <div class="flex-1 flex justify-between items-center py-2 pl-3 lg:pl-0">
        <nuxt-link to="/" class="text-blue-100 hover:text-white focus:outline-none text-lg font-bold">
          <fa :icon="['fas', 'mail-bulk']" class="inline text-gray-400 text-3xl w-10 mr-3" />
          <span class="text-2xl text-gray-400 font-light">MailAPI</span>
        </nuxt-link>
      </div>

      <label v-on:click="toggleNav" class="cursor-pointer lg:hidden block py-2 pr-4">
        <svg class="w-5 h-5 text-gray-500 hover:text-white focus:outline-none fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <title>Menu</title>
          <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"></path>
        </svg>
      </label>

      <div v-bind:class="[showNav ? 'block z-50' : 'hidden']" class="w-full border-t lg:border-0 border-gray-800 mt-2 lg:mt-0 lg:flex lg:items-center lg:w-auto">
        <ul class="lg:flex items-center justify-between text-base text-white pt-0 lg:pt-0">
          <li v-if="!userId" v-on:click="toggleNav" class="border-b lg:border-b-2 border-gray-800 lg:border-transparent lg:hover:border-white">
            <nuxt-link to="/login" class="block py-3 px-3 lg:p-4 focus:outline-none hover:bg-gray-800 lg:hover:bg-transparent">Login</nuxt-link>
          </li>
          <li v-if="!userId" v-on:click="toggleNav" class="border-b lg:border-b-2 border-gray-800 lg:border-transparent lg:hover:border-white">
            <nuxt-link to="/signup" class="block py-3 px-3 lg:p-4 focus:outline-none hover:bg-gray-800 lg:hover:bg-transparent">Signup</nuxt-link>
          </li>
          <li v-on:click="toggleNav" class="border-b lg:border-b-2 border-gray-800 lg:border-transparent lg:hover:border-white">
            <nuxt-link to="/" class="block py-3 px-3 lg:p-4 focus:outline-none hover:bg-gray-800 lg:hover:bg-transparent">tbd</nuxt-link>
          </li>
          <li v-if="userId" v-on:click="toggleNav" class="border-b lg:border-b-2 border-gray-800 lg:border-transparent lg:hover:border-white">
            <nuxt-link to="/account/overview" class="block py-3 px-3 lg:p-4 focus:outline-none hover:bg-gray-800 lg:hover:bg-transparent">Overview</nuxt-link>
          </li>
          <li v-if="userId" v-on:click="toggleNav" class="border-b lg:border-b-2 border-gray-800 lg:border-transparent lg:hover:border-white">
            <a @click="logoutSubmit" class="cursor-pointer block py-3 px-3 lg:p-4 focus:outline-none hover:bg-gray-800 lg:hover:bg-transparent">Logout</a>
          </li>
        </ul>
      </div>
    </header>
  </div>
</div>
</template>

<script>
const Cookie = require('js-cookie')

export default {
  data() {
    return {
      showNav: false,
    }
  },
  computed: {
    userId() {
      return this.$store.state.userId
    }
  },
  methods: {
    hideNav() {
      return this.showNav = false
    },
    toggleNav() {
      return this.showNav = !this.showNav
    },
    logoutSubmit() {
      this.$store.commit('updateUserId', null)
      this.$store.commit('updateAccessToken', null)
      this.$store.commit('updateRefreshToken', null)

      Cookie.remove('USER_ID')
      Cookie.remove('USER_ACCESS_TOKEN')
      Cookie.remove('USER_REFRESH_TOKEN')

      this.$router.push({
        name: 'login'
      })
    }
  }
}
</script>
