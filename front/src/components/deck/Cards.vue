<template lang="pug" src="./Cards.pug"></template>

<script>
export default {
  name: "cards",
  computed: {
    cards() {
      if (this.$store.state.currentDeck) {
          return this.$store.state.currentDeck.cards
      }
      else {
          return []
      }
    },

    columns() {
        if ((this.$store.state.currentDeck) && (this.$store.state.currentDeck.cards)) {
            var keys = [];
            var f;
            for(f in this.$store.state.currentDeck.cards[0]) {
                if (f.startsWith("_")) {
                    keys.push(f)
                }
            }
            return keys;
        } else {
          return []
      }
    }
  }
}
</script>

