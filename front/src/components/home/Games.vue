<template lang="pug" src="./Games.pug"></template>

<script>
export default {
  created: function () {
    this.$store.dispatch("retrieveGames");
  },
  computed: {
    games() {
      return this.$store.state.games;
    }
  }
}
</script>
