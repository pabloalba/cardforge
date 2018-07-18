<template lang="pug" src="./Home.pug"></template>

<script>
import MainHeader from '@/components/shared/MainHeader';
import Breadcrumbs from '@/components/shared/Breadcrumbs';
import Games from "./Games";
import { SET_CURRENT_GAME } from "../../data/store";

export default {
  name: 'home',
  components: {
    Games,
    MainHeader,
    Breadcrumbs
  },
  created: function () {
    this.$store.dispatch('retrieveMe');
    this.$store.commit(SET_CURRENT_GAME, undefined);
  }
}
</script>
