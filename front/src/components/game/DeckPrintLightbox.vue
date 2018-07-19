<template lang="pug" src="./DeckPrintLightbox.pug"></template>

<script>
import {CLOSE_LIGHTBOX} from "../../data/store";

export default {
  computed: {
    lightboxOpen() {
      return (this.$store.state.lightboxOpen === 'print-deck');
    },

    isEmpty() {
      return false;
    }
  },
  methods: {
    onSubmit() {
      console.log("PRINTTTTTTTTTTTT...");
    },
    onCancelClicked(event) {
      this.$store.commit(CLOSE_LIGHTBOX);
    }
  }
}
</script>
