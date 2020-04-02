export default {
  mode: 'universal',
  head: {
    title: '',
    meta: [{
        charset: 'utf-8'
      },
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1'
      },
      {
        hid: 'description',
        name: 'description',
        content: ''
      }
    ],
    link: [{
        rel: 'icon',
        type: 'image/x-icon',
        href: '/favicon.ico'
      },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css?family=Shadows+Into+Light&display=swap'
      }
    ]
  },
  loading: {
    color: '#0075f2'
  },
  css: [],
  plugins: [{
    src: "@/plugins/vClickOutside",
    ssr: false
  }, {
    src: "@/plugins/axiosInterceptors",
    ssr: true
  }],
  router: {
    middleware: 'router'
  },
  buildModules: [
    // Doc: https://github.com/nuxt-community/nuxt-tailwindcss
    '@nuxtjs/tailwindcss',
  ],
  modules: [
    '@nuxtjs/axios',
    ['nuxt-fontawesome', {
      component: 'fa',
      imports: [{
          set: '@fortawesome/free-solid-svg-icons',
          icons: ['fas']
        },
        {
          set: '@fortawesome/free-brands-svg-icons',
          icons: ['fab']
        }
      ]
    }]
  ],
  build: {
    extend(config, ctx) {}
  }
}
