<template lang="pug" src="./CardBuilder.pug"></template>

<script>
import MainHeader from '@/components/shared/MainHeader';
import Breadcrumbs from '@/components/shared/Breadcrumbs';
import PopupMessage from '@/components/shared/PopupMessage';

import {
  SET_SHOW_LAYERS
} from "../../data/store";

export default {
  name: 'CardBuilder',
  props: ['id'],
  components: {
    MainHeader,
    Breadcrumbs,
    PopupMessage,
  },
  created: function () {
    this.$store.commit(SET_SHOW_LAYERS, true);
    this.showPreview();

  },
  data: function () {
    return {
      cardSelected: 0,
      frontSelected: true,
      cardPreviewUrl: ""
    }
  },
  computed: {
    layersFront() {
      if (this.$store.state.currentDeck) {
          return this.$store.state.currentDeck.front_layers
      }
      else {
          return []
      }
    },

    layersBack() {
      if (this.$store.state.currentDeck) {
          return this.$store.state.currentDeck.back_layers
      }
      else {
          return []
      }
    },

    currentLayers(){
      if (this.frontSelected) {
        return this.layersFront
      } else {
        return this.layersBack
      }
    }
  },
  methods: {
    onDeleteLayerClicked(num_layer) {
      this.currentLayers.splice(num_layer,1);
    },

    onMoveUpLayerClicked(num_layer) {
      if (num_layer <= 0){
        return
      }
      var aux = this.currentLayers[num_layer];
      this.currentLayers[num_layer] = this.currentLayers[num_layer-1];
      this.currentLayers[num_layer-1] = aux;
      this.$forceUpdate();
    },

    onMoveDownLayerClicked(num_layer) {
      if (num_layer + 1 >= this.currentLayers.length){
        return
      }
      var aux = this.currentLayers[num_layer];
      this.currentLayers[num_layer] = this.currentLayers[num_layer+1];
      this.currentLayers[num_layer+1] = aux
      this.$forceUpdate();
    },

    onDuplicateLayerClicked(num_layer) {
      var item = JSON.parse(JSON.stringify(this.currentLayers[num_layer]));
      this.currentLayers.splice(num_layer, 0, item);
      this.$forceUpdate();
    },

    onAddImageLayer() {
      var item = JSON.parse('{"name":"","type":"image","x":"0","y":0,"file":"", "collapsed": false}');
      this.currentLayers.splice(0, 0, item);
      this.$forceUpdate();
    },

    onAddTextLayer() {
      var item = JSON.parse('{"name":"","type":"text","x":"0","y":0,"text":"", "color": "#FFFFFF","font": "", "font_size": 48, "collapsed": false}');
      this.currentLayers.splice(0, 0, item);
      this.$forceUpdate();
    },

    onSelectFace(face) {
      this.frontSelected = face;
      this.$forceUpdate();
      this.showPreview();
    },

    saveLayers(event) {
      this.$store.dispatch('updateLayers', {deckId: this.$store.state.currentDeck['id'], front: this.frontSelected, layers:JSON.stringify(this.currentLayers)});
      this.showPreview();
    },

    showPreview() {
      this.cardPreviewUrl = "/api/decks/"+this.$store.state.currentDeck['id']+"/forge_card?front="+this.frontSelected+"&a="+new Date().getTime();
    }
  }
}
</script>
