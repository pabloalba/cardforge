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
    editGame(game) {
      this.$store.commit(OPEN_LIGHTBOX, {name: "update-game", props: game});
    },

    cloneGame(game) {
      this.$store.dispatch("cloneGame", game.id);
    },

    deleteGame(game) {
      const callback = () => {
        this.$store.dispatch("deleteGame", game.id);
      };

      this.$store.commit(OPEN_LIGHTBOX, {name: "confirm", props: callback});
    },
  }

}
</script>
