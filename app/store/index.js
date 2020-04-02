const cookieparser = process.server ? require('cookieparser') : undefined

export const state = () => ({
  userId: null,
  accessToken: null,
  refreshToken: null
})

export const mutations = {
  updateUserId(state, userId) {
    state.userId = userId
  },
  updateAccessToken(state, accessToken) {
    state.accessToken = accessToken
  },
  updateRefreshToken(state, refreshToken) {
    state.refreshToken = refreshToken
  }
}

export const actions = {
  nuxtServerInit({
    commit
  }, {
    req
  }) {
    if (req.headers.cookie) {
      const parsed = cookieparser.parse(req.headers.cookie)

      try {
        commit('updateUserId', parsed.USER_ID)
        commit('updateAccessToken', parsed.USER_ACCESS_TOKEN)
        commit('updateRefreshToken', parsed.USER_REFRESH_TOKEN)
      } catch (err) {
        console.log('error setting cookie value to store')
      }
    }
  }
}
