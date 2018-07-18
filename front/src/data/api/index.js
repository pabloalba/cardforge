import config from '../../../cardforge-config'
import http from './http'

// TODO: handle non 200 errors

export default {
  retrieveMe() {
    return http.getJSON(`${config.API_URL}/me`);
  },

  retrieveGames() {
    return http.getJSON(`${config.API_URL}/games`);
  },

  retrieveGame(id) {
    return http.getJSON(`${config.API_URL}/games/${id}`);
  },

  retrieveGameDecks(id) {
    return http.getJSON(`${config.API_URL}/games/${id}/decks`);
  },

  retrieveDeck(id) {
    return http.getJSON(`${config.API_URL}/decks/${id}`);
  },

  async createGame(name) {
    const body = {name: name};
    const url = `${config.API_URL}/games`;

    const response = await http.post(url, body);
    return await response.json();
  }
}
