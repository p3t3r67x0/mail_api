<template>
<div class="bg-colorful bg-fixed flex flex-col min-h-screen">
  <header-component />
  <main class="mt-16 flex-grow">
    <nuxt />
  </main>
  <footer-component />
</div>
</template>

<script>
import HeaderComponent from '@/components/header.vue'
import FooterComponent from '@/components/footer.vue'

export default {
  components: {
    HeaderComponent,
    FooterComponent
  }
}
</script>
