<template lang="pug" src="./DeckCreateLightbox.pug"></template>

<script>
import {CLOSE_LIGHTBOX} from "../../data/store";

export default {
  computed: {
    lightboxOpen() {
      return (this.$store.state.lightboxOpen === 'create-deck');
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
  methods: {
    onSubmit(event) {
      event.preventDefault();
      if (this.$data.name.length > 0) {
        console.log("CREATE DECK:", this.$data.name);
      }
    },
    onCancelClicked(event) {
      this.$store.commit(CLOSE_LIGHTBOX);
    }
  }
}
</script>
