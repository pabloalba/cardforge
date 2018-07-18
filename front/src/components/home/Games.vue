<template lang="pug" src="./Games.pug"></template>

<script>
export default {
  name: "games",
  computed: {
    games() {
      return this.$store.state.games;
    }
  }
}
</script>
