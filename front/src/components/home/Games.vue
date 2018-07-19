<template lang="pug" src="./Games.pug"></template>

<script>

import {OPEN_LIGHTBOX} from "../../data/store";

export default {
  created: function () {
    this.$store.dispatch("retrieveGames");
  },

  computed: {
    games() {
      return this.$store.state.games;
    }
  },

  methods: {
    openGameUpdateLightbox(game) {
      this.$store.commit(OPEN_LIGHTBOX, {name: "update-game", props: game});
    }
  }

}
</script>
