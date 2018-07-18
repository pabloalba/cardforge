<template lang="pug" src="./Home.pug"></template>

<script>
import MainHeader from '@/components/shared/MainHeader';
import Breadcrumbs from '@/components/shared/Breadcrumbs';
import Games from "./Games";

export default {
  name: 'home',
  components: {
    Games,
    MainHeader,
    Breadcrumbs
  },
  created: function () {
    this.$store.dispatch('retrieveMe');
  }
}
</script>
