const Cookie = process.client ? require('js-cookie') : undefined

export default ({
  app,
  store
}) => {
  app.router.beforeEach((to, from, next) => {
    try {
      store.commit('updateUserId', Cookie.get('USER_ID'))
      store.commit('updateAccessToken', Cookie.get('USER_ACCESS_TOKEN'))
      store.commit('updateRefreshToken', Cookie.get('USER_REFRESH_TOKEN'))
    } catch {
      console.log('error could not fetch cookies')
    }

    next()
  })

  app.router.afterEach((to, from) => {
    // store.commit('store/updateHistoryBack', from.fullPath)
  })
}
