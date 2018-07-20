<template lang="pug" src="./Breadcrumbs.pug"></template>

<script>
import {OPEN_LIGHTBOX} from "../../data/store";

export default {
  name: "breadcrumbs",
  computed: {
    currentGame() {
      return this.$store.state.currentGame;
    },
    currentDeck() {
      return this.$store.state.currentDeck;
    },
    showLayers() {
      return this.$store.state.showLayers;
    }
  },
  methods: {
    createGame(event) {
      this.$store.commit(OPEN_LIGHTBOX, {name: "create-game"});
    },
    createDeck(event) {
      this.$store.commit(OPEN_LIGHTBOX, {name: "create-deck"});
    },
    saveLayers(event) {
      this.$emit("saveLayersEvent");
    },
    forgeCards(event) {
      this.$emit("forgeCardsEvent");
    },
    addCard(event) {
      this.$emit("addCardEvent");
    },
    saveCards(event) {
      this.$emit("saveCardsEvent");
    },
    cardDesign(event) {
      this.$emit("cardDesignEvent");
    },
    printDeck() {
      this.$store.commit(OPEN_LIGHTBOX, {name: "print-deck", props: this.currentDeck});
    }
  }
}
</script>
