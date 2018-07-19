import Vue from 'vue';
import Vuex from 'vuex';

import api from '../api';
import router from "../../router";


export const SET_ME = 'GENERAL_SET_ME';
export const SET_GAMES = 'GENERAL_SET_GAMES';
export const SET_CURRENT_GAME = 'GENERAL_SET_CURRENT_GAME';
export const SET_DECKS = 'GENERAL_SET_DECKS';
export const SET_CURRENT_DECK = 'GENERAL_SET_CURRENT_DECK';
export const SET_SHOW_LAYERS = 'GENERAL_SET_SHOW_LAYERS';

export const OPEN_LIGHTBOX = "OPEN_LIGHTBOX";
export const CLOSE_LIGHTBOX = "CLOSE_LIGHTBOX";
export const OPEN_POPUP_MESSAGE = "OPEN_POPUP_MESSAGE";
export const CLOSE_POPUP_MESSAGE = "CLOSE_POPUP_MESSAGE";

export const GAME_CREATED = "GAME_CREATED";
export const GAME_UPDATED = "GAME_UPDATED";
export const GAME_DELETED = "GAME_DELETED";

export const DECK_CREATED = "DECK_CREATED";
export const DECK_UPDATED = "DECK_UPDATED";

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
    showLayers: false,
    lightboxOpen: null,
    lightboxProps: null,
    popupMessage: null,
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

    [OPEN_POPUP_MESSAGE] (state, {header, subtext}) {
      state.popupMessage = {
        header: header,
        subtext: subtext
      };
    },

    [CLOSE_POPUP_MESSAGE] (state) {
      state.popupMessage = null;
    },
    [SET_SHOW_LAYERS] (state, show) {
      state.showLayers = show;
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

    [GAME_DELETED] (state, id) {
      state.games = state.games.filter((item) => {
        return item.id !== id;
      });

      delete state.gamesById[id];
    },

    [DECK_CREATED] (state, deck) {
      state.decks.push(deck);
      state.decksById[deck.id] = deck;
    },

    [DECK_UPDATED] (state, deck) {
      state.decks = state.decks.map((item) => {
        if (item.id === deck.id) {
          return deck;
        } else {
          return item;
        }
      });

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

    async updateGame({commit}, {id, name}) {
      const game = await api.updateGame(id, name);
      commit(GAME_UPDATED, game);
      commit(CLOSE_LIGHTBOX, null);
    },

    async deleteGame({commit}, id) {
      await api.deleteGame(id);
      commit(GAME_DELETED, id);
      commit(CLOSE_LIGHTBOX, null);
    },

    async createDeck({commit}, {gameId, name, size, orientation}) {
      const deck = await api.createDeck(gameId, name, size, orientation);
      commit(DECK_CREATED, deck);
      commit(CLOSE_LIGHTBOX, null);
    },

    async updateDeck({commit}, {id, name}) {
      const deck = await api.updateDeck(id, name);
      commit(DECK_UPDATED, deck);
      commit(CLOSE_LIGHTBOX, null);
      commit(OPEN_POPUP_MESSAGE, {
        header: "Deck updated",
        subtext: "You can edit or print the deck with the new name",
      });
    },

    async updateLayers({commit}, {deckId, front, layers}) {
      await api.updateLayers(deckId, front, layers);
    },

    async updateCards({commit}, {deckId, cards}) {
      await api.updateCards(deckId, cards);
    },

    async forgeDeck({commit}, {id, printingType, pageSize, fileType}) {
      api.forgeDeck(id, printingType, pageSize, fileType);
      commit(CLOSE_LIGHTBOX);
    },

    async handleError({commit}, error) {
      router.push("login");
    },
  }
});
