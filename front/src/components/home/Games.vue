<template lang="pug" src="./Games.pug"></template>

<script>
export default {
  name: "games",
  components: {},
  created: function () {
    console.log("Games.created", this.$store.state.games);
    this.$store.dispatch("retrieveGames");
  }
}
</script>
