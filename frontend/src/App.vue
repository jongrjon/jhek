<template>
    <div id="app">
        <header>
          <router-link to="/">
            <h1>JHEK</h1>
          </router-link>
        </header>
        <router-view />
    </div>
</template>

<script>
export default {
  name: 'App',
}
</script>