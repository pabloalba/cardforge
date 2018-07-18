<template lang="pug" src="./Game.pug"></template>

<script>
import MainHeader from '@/components/shared/MainHeader';
import Breadcrumbs from '@/components/shared/Breadcrumbs';

export default {
  name: 'game',
  props: ['id'],
  components: {
    MainHeader,
    Breadcrumbs
  },
  created: function () {
    this.$store.dispatch('retrieveGame', {id: this.id});
  }
}
</script>
