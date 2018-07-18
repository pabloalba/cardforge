<template lang="pug" src="./Breadcrumbs.pug"></template>

<script>
export default {
  name: 'breadcrumbs',
  computed: {
    currentGame: function () {
      return this.$store.state.currentGame;
    }
  }
}
</script>
