<template>
  <div id="nav">
    <router-link to="/welcome/">Home</router-link> |
    <router-link to="/welcome/about">About</router-link> |
    <router-link to="/">Back</router-link>
  </div>
  <router-view/>
</template>

<script>
export default {
  name: "Welcome"
}
</script>

<style scoped>

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>