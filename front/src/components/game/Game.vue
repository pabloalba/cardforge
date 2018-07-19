<template lang="pug" src="./Game.pug"></template>

<script>
import MainHeader from '@/components/shared/MainHeader';
import Breadcrumbs from '@/components/shared/Breadcrumbs';
import PopupMessage from '@/components/shared/PopupMessage';
import Decks from "./Decks";
import DeckCreateLightbox from "./DeckCreateLightbox";
import DeckUpdateLightbox from "./DeckUpdateLightbox";
import DeckPrintLightbox from "./DeckPrintLightbox";

import {
  SET_GAMES, SET_DECKS, SET_CURRENT_GAME, SET_CURRENT_DECK
} from "../../data/store";

export default {
  name: 'game',
  props: ['id'],
  components: {
    MainHeader,
    Breadcrumbs,
    PopupMessage,
    Decks,
    DeckCreateLightbox,
    DeckUpdateLightbox,
    DeckPrintLightbox
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
