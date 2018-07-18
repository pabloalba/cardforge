<template lang="pug" src="./MainHeader.pug"></template>

<script>
export default {
  name: 'main-header',
  computed: {
    me: function () {
      return this.$store.getters.getMe;
    }
  }
}
</script>
