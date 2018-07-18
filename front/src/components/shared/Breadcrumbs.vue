<template lang="pug" src="./Breadcrumbs.pug"></template>

<script>
import {OPEN_GAME_CREATE_LIGHBOX} from "../../data/store";

export default {
  name: 'breadcrumbs',
  computed: {
    currentGame: function () {
      return this.$store.state.currentGame;
    },
    currentDeck: function () {
      return this.$store.state.currentDeck;
    }
  },
  methods: {
    openGameCreateLighbox(event) {
      event.preventDefault();
      this.$store.commit(OPEN_GAME_CREATE_LIGHBOX, null);
    }
  }
}
</script>
