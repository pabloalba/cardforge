<template lang="pug" src="./Decks.pug"></template>

<script>
import {OPEN_LIGHTBOX} from "../../data/store";

export default {
  name: "decks",
  computed: {
    decks() {
      return this.$store.state.decks;
    }
  },
  methods: {
    openDeckUpdateLightbox(deck) {
      this.$store.commit(OPEN_LIGHTBOX, {name: "update-deck", props: deck});
    },
    openPrintLightbox(deck) {
      this.$store.commit(OPEN_LIGHTBOX, {name: "print-deck", props: deck});
    }
  }
}
</script>
