<template lang="pug" src="./Breadcrumbs.pug"></template>

<script>
import {OPEN_LIGHTBOX} from "../../data/store";

export default {
  name: 'breadcrumbs',
  computed: {
    currentGame: function () {
      return this.$store.state.currentGame;
    },
    currentDeck: function () {
      return this.$store.state.currentDeck;
    },
    showLayers: function () {
      return this.$store.state.showLayers;
    }
  },
  methods: {
    openGameCreateLighbox(event) {
      this.$store.commit(OPEN_LIGHTBOX, {name: "create-game"});
    },
    openDeckCreateLighbox(event) {
      this.$store.commit(OPEN_LIGHTBOX, {name: "create-deck"});
    }
  }
}
</script>
