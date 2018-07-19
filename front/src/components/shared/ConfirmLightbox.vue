<template lang="pug" src="./ConfirmLightbox.pug"></template>

<script>
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
    onOkClicked() {
      this.$store.commit(CLOSE_LIGHTBOX);
    }
  }
}
</script>
