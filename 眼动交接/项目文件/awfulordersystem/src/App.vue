<template>
  <router-view/>
</template>

<script>
  export default {
    name: 'App',
    mounted() {
      window.onunload = () => {
        // send a message to /api/leave using Beacon API
        navigator.sendBeacon('/api/stop_record');
      };
    }
  }
</script>