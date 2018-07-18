import Vue from 'vue';
import Vuex from 'vuex';

import api from '../api';

export const SET_ME = 'GENERAL_SET_ME';
export const SET_GAMES = 'GENERAL_SET_GAMES';
export const SET_CURRENT_GAME = 'GENERAL_SET_CURRENT_GAME';
export const SET_DECKS = 'GENERAL_SET_DECKS';
export const SET_CURRENT_DECK = 'GENERAL_SET_CURRENT_DECK';

export const OPEN_LIGHTBOX = "OPEN_LIGHTBOX";
export const CLOSE_LIGHTBOX = "CLOSE_LIGHTBOX";

export const GAME_CREATED = "GAME_CREATED";
export const DECK_CREATED = "DECK_CREATED";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    me: null,
    games: [],
    gamesById: {},
    currentGame: null,
    decks: null,
    decksById: {},
    currentDeck: null,
    lightboxOpen: null,
    lightboxProps: null,
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

    [OPEN_LIGHTBOX] (state, {name, props=null}) {
      state.lightboxOpen = name;
      state.lightboxProps = props;
    },

    [CLOSE_LIGHTBOX] (state) {
      state.lightboxOpen = null;
      state.lightboxProps = null;
    },

    [GAME_CREATED] (state, game) {
      state.games.push(game);
      state.gamesById[game.id] = game;
    },

    [GAME_UPDATED] (state, game) {
      state.games = state.games.map((item) => {
        if (item.id === game.id) {
          return game;
        } else {
          return item;
        }
      });

      state.gamesById[game.id] = game;
    },

    [DECK_CREATED] (state, deck) {
      state.decks.push(deck);
      state.decksById[deck.id] = deck;
    },
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
    },

    async createGame({commit}, {name}) {
      const game = await api.createGame(name);
      commit(GAME_CREATED, game);
      commit(CLOSE_LIGHTBOX, null);
    },

    async updateGame({commit}, game) {
      game = await api.createGame(game);
      commit(GAME_UPDATED, game);
      commit(CLOSE_LIGHTBOX, null);
    },

    async createDeck({commit}, {gameId, name, size, orientation}) {
      const deck = await api.createDeck(gameId, name, size, orientation);
      commit(DECK_CREATED, deck);
      commit(CLOSE_LIGHTBOX, null);
    }
  }
});
