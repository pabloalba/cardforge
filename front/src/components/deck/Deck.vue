<template lang="pug" src="./Deck.pug"></template>

<script>
import MainHeader from '@/components/shared/MainHeader';
import Breadcrumbs from '@/components/shared/Breadcrumbs';
import PopupMessage from '@/components/shared/PopupMessage';
import Cards from "./Cards";

import {
  SET_SHOW_LAYERS
} from "../../data/store";

export default {
  name: 'deck',
  props: ['id'],
  components: {
    MainHeader,
    Breadcrumbs,
    PopupMessage,
    Cards
  },
  created: function () {
    this.$store.commit(SET_SHOW_LAYERS, false);
    this.$store.dispatch('retrieveDeck', {id: this.id});
  }
}
</script>
