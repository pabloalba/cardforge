<template lang="pug" src="./Game.pug"></template>

<script>
import MainHeader from '@/components/shared/MainHeader';
import Breadcrumbs from '@/components/shared/Breadcrumbs';
import Decks from "./Decks";
import {
  SET_GAMES, SET_DECKS, SET_CURRENT_GAME, SET_CURRENT_DECK
} from "../../data/store";

export default {
  name: 'game',
  props: ['id'],
  components: {
    MainHeader,
    Breadcrumbs,
    Decks
  },
  created: function () {
    this.$store.commit(SET_GAMES, null);
    this.$store.commit(SET_DECKS, null);
    this.$store.commit(SET_CURRENT_GAME, null);
    this.$store.commit(SET_CURRENT_DECK, undefined);
    this.$store.dispatch('retrieveGame', {id: this.id});
    this.$store.dispatch('retrieveGameDecks', {id: this.id});
  }
}
</script>
