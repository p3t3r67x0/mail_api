export default function({
  store,
  redirect,
  route
}) {
  const userId = store.state.userId
  const urlRequiresAuth = /^\/account(\/|$)/.test(route.fullPath)
  const urlRequiresNonAuth = /^\/login(\/|$)/.test(route.fullPath)

  if (!userId && urlRequiresAuth) {
    return redirect('/login')
  }
  if (userId && urlRequiresNonAuth) {
    return redirect('/account/overview')
  }

  return Promise.resolve()
}
