<template lang="pug" src="./Deck.pug"></template>

<script>
import MainHeader from '@/components/shared/MainHeader';
import Breadcrumbs from '@/components/shared/Breadcrumbs';
import PopupMessage from '@/components/shared/PopupMessage';
import Cards from "./Cards";
import router from "@/router"

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
  },
  methods: {
    addCard() {
      if (this.$store.state.currentDeck) {
          var name = "CARD "+(this.$store.state.currentDeck.cards.length + 1);
          this.$store.state.currentDeck.cards.push(JSON.parse('{"name": "'+name+'"}'));
      }
    },
    saveCards() {
      if (this.$store.state.currentDeck) {
          this.$store.dispatch('updateCards', {deckId: this.$store.state.currentDeck['id'], cards:JSON.stringify(this.$store.state.currentDeck.cards)});
      }
    },
    cardDesign() {
      if (this.$store.state.currentDeck) {
        this.saveCards();
        router.push({ name: "card-builder", params: {id: this.$store.state.currentDeck['id']} });
      }

    },
  }
}
</script>
