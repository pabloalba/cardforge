<template lang="pug" src="./Decks.pug"></template>

<script>
export default {
  name: "decks",
  computed: {
    decks() {
      return this.$store.state.decks;
    }
  }
}
</script>
