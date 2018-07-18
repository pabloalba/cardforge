import Vue from 'vue';
import Vuex from 'vuex';

import api from '../api';

export const SET_ME = 'GENERAL_SET_ME';
export const SET_GAMES = 'GENERAL_SET_GAMES';
export const SET_CURRENT_GAME = 'GENERAL_SET_CURRENT_GAME';
export const SET_DECKS = 'GENERAL_SET_DECKS';
export const SET_CURRENT_DECK = 'GENERAL_SET_CURRENT_DECK';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    me: null,
    games: null,
    currentGame: null,
    decks: null,
    currentDeck: null
  },

  mutations: {
    [SET_ME] (state, me) {
      state.me = me;
    },
    [SET_GAMES] (state, games) {
      state.games = games;
    },
    [SET_CURRENT_GAME] (state, game) {
      state.currentGame = game;
    },
    [SET_DECKS] (state, decks) {
      state.decks = decks;
    },
    [SET_CURRENT_DECK] (state, deck) {
      state.currentDeck = deck;
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
    },

    async retrieveGame({commit}, {id}) {
      const game = await api.retrieveGame(id);
      commit(SET_CURRENT_GAME, game);
    },

    async retrieveGameDecks({commit}, {id}) {
      const decks = await api.retrieveGameDecks(id);
      commit(SET_DECKS, decks);
    },

    async retrieveDeck({commit}, {id}) {
      const deck = await api.retrieveDeck(id);
      commit(SET_CURRENT_DECK, deck);
    }
  }
})
