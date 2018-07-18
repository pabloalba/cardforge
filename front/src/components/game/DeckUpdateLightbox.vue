<template lang="pug" src="./DeckUpdateLightbox.pug"></template>

<script>
import {CLOSE_LIGHTBOX} from "../../data/store";

export default {
  computed: {
    lightboxOpen() {
      return this.$store.state.lightboxOpen;
    },

    deckName() {
      return this.$store.state.lightboxProps ? this.$store.state.lightboxProps.name : null;
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
    deckName(name) {
      console.log('eeee');
      this.name = name;
    }
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      if (this.$data.name.length > 0) {
        console.log("UPDATE DECK:", this.$data.name);
      }
    },
    onCancelClicked() {
      this.$store.commit(CLOSE_LIGHTBOX);
    }
  }
}
</script>
