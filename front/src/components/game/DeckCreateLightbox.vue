<template lang="pug" src="./DeckCreateLightbox.pug"></template>

<script>
import {CLOSE_LIGHTBOX} from "../../data/store";

export default {
  computed: {
    lightboxOpen() {
      return (this.$store.state.lightboxOpen === 'create-deck');
    },

    gameId() {
      return this.$store.state.currentGame.id;
    },

    isEmpty() {
      return (this.name.length === 0) ||
        (this.size.length === 0) ||
        (this.orientation.length === 0);
    }
  },
  data() {
    return {
      errors: [],
      name: "",
      size: "",
      orientation: "",
    }
  },
  methods: {
    onSubmit() {
      this.$store.dispatch("createDeck", {
        gameId: this.gameId,
        name: this.name,
        size: this.size,
        orientation: this.orientation
      });
    },
    onCancelClicked(event) {
      this.$store.commit(CLOSE_LIGHTBOX);
    }
  }
}
</script>
