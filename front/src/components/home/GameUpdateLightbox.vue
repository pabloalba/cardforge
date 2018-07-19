<template lang="pug" src="./GameUpdateLightbox.pug"></template>

<script>

import {CLOSE_LIGHTBOX} from "../../data/store";

export default {
  computed: {
    isHidden() {
      return this.$store.state.lightboxOpen != "update-game";
    },

    currentGame() {
      return this.$store.state.lightboxProps;
    },

    propsName() {
      const props = this.$store.state.lightboxProps;
      return props ? props.name : null;
    },

    isNameEmpty() {
      const name = this.$data.name || "";
      return name.length == 0;
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
        this.$store.dispatch("updateGame", {
          id: this.currentGame.id,
          name: this.name,
        });
      }
    },
    onCancelClicked() {
      this.$store.commit(CLOSE_LIGHTBOX);
    }
  }
}
</script>
