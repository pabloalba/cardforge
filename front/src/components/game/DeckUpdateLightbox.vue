<template lang="pug" src="./DeckUpdateLightbox.pug"></template>

<script>
import {CLOSE_LIGHTBOX} from "../../data/store";

export default {
  computed: {
    lightboxOpen() {
      return (this.$store.state.lightboxOpen === 'update-deck');
    },

    propsName() {
      const props = this.$store.state.lightboxProps;
      return props ? props.name : null;
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
    propsName(newName, oldName) {
      this.name = newName;
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
