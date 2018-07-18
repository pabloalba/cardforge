import Vue from 'vue';
import Vuex from 'vuex';

import api from '../api';

export const SET_ME = 'GENERAL_SET_ME';
export const SET_GAMES = 'GENERAL_SET_GAMES';


Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    me: null,
    games: null
  },

  mutations: {
    [SET_ME] (state, me) {
      state.me = me;
    },
    [SET_GAMES] (state, games) {
      console.log("SET_GAMES", games);
      state.games = games;
    }
  },

  actions: {
    async retrieveMe({commit}) {
      const me = await api.retrieveMe();
      commit(SET_ME, me)
    },

    async retrieveGames({commit}) {
      let games = await api.retrieveGames();
      // let games = [{
      //   name: "Test1",
      //   decks: 3
      // }, {
      //   name: "Test2",
      //   decks: 2
      // }];

      commit(SET_GAMES, games);
    }
  }
})
