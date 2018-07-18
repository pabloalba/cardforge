import config from '../../../cardforge-config'
import http from './http'

export default {
  retrieveMe() {
    return http.fetch('GET', `${config.API_URL}/me`);
  },
  retrieveGames() {
    return http.fetch('GET', `${config.API_URL}/games`);
  },
  retrieveGame(id) {
    return http.fetch('GET', `${config.API_URL}/games/${id}`);
  },
  retrieveGameDecks(id) {
    return http.fetch('GET', `${config.API_URL}/games/${id}/decks`);
  },
  retrieveDeck(id) {
    return http.fetch('GET', `${config.API_URL}/decks/${id}`);
  }
}
