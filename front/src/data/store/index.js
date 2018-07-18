import Vue from 'vue';
import Vuex from 'vuex';

import api from '../api';

export const SET_ME = 'GENERAL_SET_ME';
export const SET_GAMES = 'GENERAL_SET_GAMES';
export const SET_CURRENT_GAME = 'GENERAL_SET_CURRENT_GAME';
export const SET_DECKS = 'GENERAL_SET_DECKS';
export const SET_CURRENT_DECK = 'GENERAL_SET_CURRENT_DECK';

export const OPEN_GAME_CREATE_LIGHBOX = "OPEN_GAME_CREATE_LIGHBOX";
export const OPEN_GAME_UPDATE_LIGHBOX = "OPEN_GAME_UPDATE_LIGHBOX";
export const CLOSE_GAME_CREATE_LIGHBOX = "CLOSE_GAME_CREATE_LIGHBOX";
export const CLOSE_GAME_UPDATE_LIGHBOX = "CLOSE_GAME_UPDATE_LIGHBOX";

export const GAME_CREATED = "GAME_CREATED";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    me: null,
    games: [],
    gamesById: {},
    currentGame: null,
    decks: null,
    currentDeck: null,
    gameCreateLightbox: null,
    gameUpdateLightbox: null
  },

  mutations: {
    [SET_ME] (state, me) {
      state.me = me;
    },
    [SET_GAMES] (state, games) {
      if (games) {
        state.games = games;
        state.gamesById = games.reduce((acc, item) => {
          return Object.assign(acc, {[item.id]: item});
        }, {});
      }
    },

    [SET_CURRENT_GAME] (state, game) {
      state.currentGame = game;
    },

    [SET_DECKS] (state, decks) {
      state.decks = decks;
    },

    [SET_CURRENT_DECK] (state, deck) {
      state.currentDeck = deck;
    },

    [OPEN_GAME_CREATE_LIGHBOX] (state) {
      state.gameCreateLightbox = {
        isHidden: false
      };
    },

    [CLOSE_GAME_CREATE_LIGHBOX] (state) {
      state.gameCreateLightbox = null;
    },

    [OPEN_GAME_UPDATE_LIGHBOX] (state, id) {
      state.gameUpdateLightbox = {
        isHidden: false,
        id: id
      };
    },

    [CLOSE_GAME_UPDATE_LIGHBOX] (state) {
      state.gameCreateLightbox = null;
    },

    [GAME_CREATED] (state, game) {
      state.games.push(game);
      state.gamesById[game.id] = game;
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

    async createGame({commit}, {name}) {
      const game = await api.createGame(name);
      commit(GAME_CREATED, game);
    }
  }
})
