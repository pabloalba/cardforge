<template lang="pug" src="./PrintInfoLightbox.pug"></template>

<script>
import {CLOSE_LIGHTBOX} from "../../data/store";

export default {
  computed: {
    lightboxOpen() {
      return (this.$store.state.lightboxOpen === 'print-info');
    }
  },
  methods: {
    onCloseClicked() {
      this.$store.commit(CLOSE_LIGHTBOX);
    }
  }
}
</script>
