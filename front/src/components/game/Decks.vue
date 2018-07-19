<template lang="pug" src="./Decks.pug"></template>

<script>
import {OPEN_LIGHTBOX, DECK_SIZES} from "../../data/store";

export default {
  computed: {
    decks() {
      return this.$store.state.decks;
    }
  },
  methods: {
    updateDeck(deck) {
      this.$store.commit(OPEN_LIGHTBOX, {name: "update-deck", props: deck});
    },

    cloneDeck(deck) {
      this.$store.dispatch("cloneDeck", deck.id);
    },

    printDeck(deck) {
      this.$store.commit(OPEN_LIGHTBOX, {name: "print-deck", props: deck});
    },

    deleteDeck(deck) {
      this.$store.commit(OPEN_LIGHTBOX, {name: "confirm", props: deck});
    },

    deckSizeName(size){
      return DECK_SIZES[size];
    }
  }
}
</script>
