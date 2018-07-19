<template lang="pug" src="./Cards.pug"></template>

<script>
export default {
  name: "cards",
  computed: {
    cards() {
      if (this.$store.state.currentDeck) {
          return this.$store.state.currentDeck.cards
      }
      else {
          return []
      }
    },

    columns() {
        if (this.$store.state.currentDeck) {
            var keys = [];
            var layer;
            var i;
            if (this.$store.state.currentDeck.front_layers) {
                for(i=0;i<this.$store.state.currentDeck.front_layers.length;i++) {
                    var layer = this.$store.state.currentDeck.front_layers[i];
                    if (!layer['template']) {
                        keys.push({
                            "name": layer['name'],
                            "id": layer['id']
                        })
                    }
                }
            }

            if (this.$store.state.currentDeck.back_layers) {
                for(i=0;i<this.$store.state.currentDeck.back_layers.length;i++) {
                    var layer = this.$store.state.currentDeck.back_layers[i];
                    if (!layer['template']) {
                        keys.push({
                            "name": layer['name'],
                            "id": layer['id']
                        })
                    }
                }
            }
            return keys;
        } else {
          return []
      }
    }
  },
  methods: {
      onDuplicateCardClicked(num_card) {
          if (this.cards){
            var item = JSON.parse(JSON.stringify(this.cards[num_card]));
            item['name'] += "_1";
            this.cards.splice(num_card+1, 0, item);
            this.$forceUpdate();
          }
      },
      onDeleteCardClicked(num_card) {
        this.cards.splice(num_card,1);
        this.$forceUpdate();
    },
  }
}
</script>

