<template lang="pug" src="./DeckUpdateLightbox.pug"></template>

<script>
import {CLOSE_LIGHTBOX} from "../../data/store";

export default {
  computed: {
    lightboxOpen() {
      return (this.$store.state.lightboxOpen === 'update-deck');
    },

    currentDeck() {
      return this.$store.state.lightboxProps;
    },

    isNameEmpty() {
      return this.$data.name.length == 0;
    }
  },
  data() {
    return {
      errors: [],
      name: ""
    }
  },
  watch: {
    currentDeck(newDeck, oldDeck) {
      this.name = newDeck ? newDeck.name : null;
    }
  },
  methods: {
    onSubmit() {
      this.$store.dispatch("updateDeck", {
        id: this.currentDeck.id,
        name: this.name,
      });
    },
    onCancelClicked() {
      this.$store.commit(CLOSE_LIGHTBOX);
    }
  }
}
</script>
