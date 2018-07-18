import Vue from 'vue';
import Vuex from 'vuex';

import api from '../api';

export const SET_ME = Symbol('set-me');
export const SET_GAMES = Symbol('set-games');


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
      state.games = games;
    }
  },

  actions: {
    async retrieveMe({commit}) {
      const me = await api.retrieveMe();
      commit(SET_ME, me)
    },

    async retrieveGames({commit}) {
      const games = await api.retrieveGames();
      commit(SET_GAMES, games);
    }
  }
})
