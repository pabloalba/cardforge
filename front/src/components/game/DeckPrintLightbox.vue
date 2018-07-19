<template lang="pug" src="./DeckPrintLightbox.pug"></template>

<script>
import {CLOSE_LIGHTBOX} from "../../data/store";

export default {
  computed: {
    lightboxOpen() {
      return (this.$store.state.lightboxOpen === "print-deck");
    },

    isEmpty() {
      return (this.printingType.length === 0) ||
        (this.pageSize.length === 0 && this.printingType !== "tabletop") ||
        (this.fileType.length === 0 && this.printingType !== "tabletop");
    },

    disableOptions() {
      return (this.printingType === "tabletop");
    }
  },
  data() {
    return {
      printingType: "",
      pageSize: "",
      fileType: "",
    }
  },
  watch: {
    lightboxOpen(newOpen, oldOpen) {
      if (newOpen) {
        this.printingType = "";
        this.pageSize = "";
        this.fileType = "";
      }
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
