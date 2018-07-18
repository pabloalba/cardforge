<template lang="pug" src="./GameCreateLightbox.pug"></template>

<script>
import {CLOSE_LIGHTBOX} from "../../data/store";

export default {
  computed: {
    isHidden() {
      return this.$store.state.lightboxOpen != "create-game";
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
        this.$store.dispatch("createGame", {name: this.$data.name});
      }
    },
    onCancelClicked(event) {
      this.$store.commit(CLOSE_LIGHTBOX, null);
    }
  }
}
</script>
