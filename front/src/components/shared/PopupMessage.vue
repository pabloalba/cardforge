<template lang="pug" src="./PopupMessage.pug"></template>

<script>
import {CLOSE_POPUP_MESSAGE} from "../../data/store";

export default {
  computed: {
    messageOpen() {
      return !!this.$store.state.popupMessage;
    },

    messageHeader() {
      const message = this.$store.state.popupMessage;
      return message? message.header : null;
    },

    messageSubtext() {
      const message = this.$store.state.popupMessage;
      return message? message.subtext : null;
    },
  },
  watch: {
    messageOpen(newOpen, oldOpen) {
      if (newOpen) {
        setTimeout(() => {
          this.onCloseClicked();
        }, 5000);
      }
    }
  },
  methods: {
    onCloseClicked() {
      this.$store.commit(CLOSE_POPUP_MESSAGE);
    }
  }
}
</script>
