<template lang="pug" src="./Home.pug"></template>

<script>
import MainHeader from '@/components/shared/MainHeader';
import Breadcrumbs from '@/components/shared/Breadcrumbs';
import PopupMessage from '@/components/shared/PopupMessage';
import Games from "./Games";

import GameCreateLightbox from "./GameCreateLightbox";
import GameUpdateLightbox from "./GameUpdateLightbox";

import {
  SET_GAMES, SET_DECKS, SET_CURRENT_GAME, SET_CURRENT_DECK
} from "../../data/store";

export default {
  name: 'home',
  components: {
    Games,
    MainHeader,
    Breadcrumbs,
    PopupMessage,
    Games,
    GameCreateLightbox,
    GameUpdateLightbox
  },
  created: function () {
    this.$store.commit(SET_GAMES, null);
    this.$store.commit(SET_DECKS, null);
    this.$store.commit(SET_CURRENT_GAME, undefined);
    this.$store.commit(SET_CURRENT_DECK, undefined);
    this.$store.dispatch("retrieveMe");
    this.$store.dispatch("retrieveGames");
  }
}
</script>
