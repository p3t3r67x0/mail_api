const Cookie = process.client ? require('js-cookie') : undefined

export default ({
  app,
  store
}) => {
  app.$axios.defaults.headers.get['Content-Type'] = 'application/json'
  app.$axios.defaults.headers.put['Content-Type'] = 'application/json'
  app.$axios.defaults.headers.post['Content-Type'] = 'application/json'
  app.$axios.defaults.headers.delete['Content-Type'] = 'application/json'

  app.$axios.interceptors.request.use(
    function(config) {
      // store.commit('store/updateLoadingIndicator', true)
      // console.log('updateLoadingIndicator: ' + store.state.loading)

      if (config.url.includes('/api/v1/token/refresh')) {
        const refreshToken = Cookie.get('USER_REFRESH_TOKEN')

        if (refreshToken) {
          config.headers.Authorization = 'Bearer ' + refreshToken
        }
      } else {
        const accessToken = Cookie.get('USER_ACCESS_TOKEN')

        if (accessToken) {
          store.commit('updateUserId', Cookie.get('USER_ID'))
          config.headers.Authorization = 'Bearer ' + accessToken
        }
      }

      return config
    },
    function(error) {
      // store.commit('store/updateLoadingIndicator', false)
      // console.log('updateLoadingIndicator: ' + store.state.loading)
      return Promise.reject(error)
    }
  )

  app.$axios.interceptors.response.use(
    function(response) {
      // store.commit('store/updateLoadingIndicator', false)
      // console.log('updateLoadingIndicator: ' + store.state.loading)
      return response
    },
    function(error) {
      if (error.config && error.response && error.response.status === 401) {
        const refreshUrl = process.env.API_URL + '/api/v1/token/refresh'
        const refreshToken = Cookie.get('USER_REFRESH_TOKEN')

        if (refreshToken) {
          return app.$axios.post(refreshUrl, {}, {
              headers: {
                'Authorization': 'Bearer ' + refreshToken
              }
            }).then((response) => {
              // store.commit('store/updateLoadingIndicator', false)
              // console.log('updateLoadingIndicator: ' + store.state.loading)

              store.commit('updateAccessToken', response.data.access_token)
              Cookie.set('USER_ACCESS_TOKEN', response.data.access_token)

              error.config.headers.Authorization = 'Bearer ' + response.data.access_token
              return app.$axios.request(error.config)
            })
            .catch((error) => {
              // store.commit('store/updateLoadingIndicator', false)
              // console.log('updateLoadingIndicator: ' + store.state.loading)
              return Promise.reject(error)
            })
        }
      }

      // store.commit('store/updateLoadingIndicator', false)
      // console.log('updateLoadingIndicator: ' + store.state.loading)
      return Promise.reject(error)
    }
  )
}
