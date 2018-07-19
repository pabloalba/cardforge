<template lang="pug" src="./CardBuilder.pug"></template>

<script>
import MainHeader from '@/components/shared/MainHeader';
import Breadcrumbs from '@/components/shared/Breadcrumbs';
import PopupMessage from '@/components/shared/PopupMessage';
import PrintInfoLightbox from "./PrintInfoLightbox";
import router from "@/router"


import {
  SET_SHOW_LAYERS,
  DECK_SIZES,
  GENERATE_DESIGN_PREVIEW_URL,
  CLEAR_DESIGN_PREVIEW_URL
} from "../../data/store";

import {OPEN_LIGHTBOX} from "../../data/store";

export default {
  name: 'CardBuilder',
  props: ['id'],
  components: {
    MainHeader,
    Breadcrumbs,
    PopupMessage,
    PrintInfoLightbox,
  },
  created: function () {
    this.$store.commit(SET_SHOW_LAYERS, true);
    this.frontSelected = true;
    this.refreshPreview();
    if (this.$store.state.currentDeck.portrait) {
      this.cardGuidesUrl = require("../../images/guides/"+this.$store.state.currentDeck.size.toLowerCase()+"b.png");
    } else {
      this.cardGuidesUrl = require("../../images/guides/"+this.$store.state.currentDeck.size.toLowerCase()+".png");
    }
    this.guidesRotated = this.$store.state.currentDeck['portrait']
  },
  destroyed: function () {
    this.$store.commit(CLEAR_DESIGN_PREVIEW_URL);
  },
  data: function () {
    return {
      cardSelected: 0,
      frontSelected: true,
      cardGuidesUrl: "",
      showGuides: false,
      guidesRotated: false,
      loadingPreview: false,
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

    currentLayers() {
      if (this.frontSelected) {
        return this.layersFront
      } else {
        return this.layersBack
      }
    },

    deskDescription() {
      var portrait = "Landscape";
      // TODO: Bug on back, portrait and landscape are inverted
      if (!this.$store.state.currentDeck.portrait) {
        portrait = "Portrait";
      }

      return DECK_SIZES[this.$store.state.currentDeck.size] + " | " + portrait;
    },

    cardPreviewUrl() {
      return this.$store.state.designPreviewUrl;
    }
  },
  watch: {
    cardPreviewUrl(newUrl, oldUrl) {
      if (newUrl) {
        this.loadingPreview = true;
      }
    }
  },
  methods: {
    onDeleteLayerClicked(num_layer) {
      this.currentLayers.splice(num_layer,1);
      this.$forceUpdate();
    },

    onCollapseLayerClicked(num_layer) {
      this.currentLayers[num_layer]['collapsed'] = !this.currentLayers[num_layer]['collapsed'];
      this.$forceUpdate();
    },

    onSetVisibleLayer(num_layer, visible) {
      this.currentLayers[num_layer]['visible'] = visible;
      this.$forceUpdate();
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
      var i;
      var num = 1;
      for (i=0;i<this.currentLayers.length;i++){
        if (this.currentLayers[i]['type'] === 'image'){
          num += 1;
        }
      }
      var name = "IMAGE "+ num;
      var id = "layer_" + new Date().getTime();
      var item = JSON.parse('{"id":"' + id + '", "name":"' + name + '","type":"image","visible": true,"x":"0","y":0,"file":"", "collapsed": false, "template": true}');
      this.currentLayers.splice(0, 0, item);
      this.$forceUpdate();
    },

    onAddTextLayer() {
      var i;
      var num = 1;
      for (i=0;i<this.currentLayers.length;i++){
        if (this.currentLayers[i]['type'] === 'text'){
          num += 1;
        }
      }
      var name = "TEXT "+ num;
      var id = "layer_" + new Date().getTime();
      var item = JSON.parse('{"id":"' + id + '", "name":"' + name + '","type":"text","visible": true,"x":"0","y":0,"text":"", "color": "#FFFFFF","font": "", "font_size": 48, "collapsed": false, "template": true}');
      this.currentLayers.splice(0, 0, item);
      this.$forceUpdate();
    },

    refreshPreview() {
      this.$store.commit(GENERATE_DESIGN_PREVIEW_URL, {front: this.frontSelected});
    },

    onPreviewLoaded() {
      this.loadingPreview = false;
    },

    onSelectFace(face) {
      this.frontSelected = face;
      this.$forceUpdate();
      this.refreshPreview();
    },

    saveLayers(event) {
      this.$store.dispatch('updateLayers', {deckId: this.$store.state.currentDeck['id'], front: this.frontSelected, layers:JSON.stringify(this.currentLayers)});
    },

    onPrintInfoClicked() {
      this.$store.commit(OPEN_LIGHTBOX, {name: "print-info"});
    },

    forgeCards() {
      this.saveLayers();
      router.push({ name: "deck", params: {id: this.$store.state.currentDeck['id']} });
    }
  }
}
</script>
