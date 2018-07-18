<template lang="pug" src="./GameCreateLightbox.pug"></template>

<script>
import {CLOSE_GAME_CREATE_LIGHBOX} from "../../data/store";

export default {
  computed: {
    isHidden() {
      const state = this.$store.state.gameCreateLightbox;
      return state ? state.isHidden : true;
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
      this.$store.commit(CLOSE_GAME_CREATE_LIGHBOX, null);
    }
  }
}
</script>
