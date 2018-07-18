<template lang="pug" src="./Game.pug"></template>

<script>
import MainHeader from '@/components/shared/MainHeader';
import Breadcrumbs from '@/components/shared/Breadcrumbs';
import Decks from "./Decks";
import { SET_CURRENT_DECK } from "../../data/store";

export default {
  name: 'game',
  props: ['id'],
  components: {
    MainHeader,
    Breadcrumbs,
    Decks
  },
  created: function () {
    this.$store.dispatch('retrieveGame', {id: this.id});
    this.$store.dispatch('retrieveGameDecks', {id: this.id});
    this.$store.commit(SET_CURRENT_DECK, undefined);
  }
}
</script>
