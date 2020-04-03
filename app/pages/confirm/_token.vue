<template>
</template>

<script>
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
  created() {
    this.$axios.$post(process.env.API_URL + '/api/v1/confirm', {
      'token': this.token.trim()
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
  },
  computed: {
    token() {
      return this.$route.params.token
    }
  },
  middleware: 'auth'
}
</script>
