<template lang="pug" src="./ConfirmLightbox.pug"></template>

<script>
import {isFunction} from "lodash";
import {CLOSE_LIGHTBOX} from "../../data/store";

export default {
  computed: {
    lightboxOpen() {
      return (this.$store.state.lightboxOpen === 'confirm');
    }
  },
  methods: {
    onCancelClicked() {
      this.$store.commit(CLOSE_LIGHTBOX);
    },

    async onOkClicked() {
      if (isFunction(this.$store.state.lightboxProps)) {
        await this.$store.state.lightboxProps();
      }
      this.$store.commit(CLOSE_LIGHTBOX);
    }
  }
}
</script>
