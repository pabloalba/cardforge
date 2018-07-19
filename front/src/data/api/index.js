import config from '../../../cardforge-config'
import http from './http'

// TODO: handle non 200 errors

function pickBody(rsp) {
  return rsp.body;
}

export default {
  retrieveMe() {
    return http.get(`${config.API_URL}/me`).then(pickBody);
  },

  retrieveGames() {
    return http.get(`${config.API_URL}/games`).then(pickBody);
  },

  retrieveGame(id) {
    return http.get(`${config.API_URL}/games/${id}`).then(pickBody);
  },

  retrieveGameDecks(id) {
    return http.get(`${config.API_URL}/games/${id}/decks`).then(pickBody);
  },

  retrieveDeck(id) {
    return http.get(`${config.API_URL}/decks/${id}`).then(pickBody);
  },

  async createGame(name) {
    const body = {name: name};
    const url = `${config.API_URL}/games`;

    const response = await http.post(url, body);
    return await response.json();
  },

  async updateGame(id, name) {
    const body = {id, name};
    const url = `${config.API_URL}/games/${id}`;
    const response = await http.patch(url, body);
    return await response.json();
  },

  async deleteGame(id) {
    const url = `${config.API_URL}/games/${id}`;
    const response = await http.delete(url);
    return null;
  },

  async createDeck(gameId, name, size, orientation) {
    const body = {
      name: name,
      size: size,
      portrait: orientation === "portrait" ? true : false,
      front_cut_marks_color: "#ff0000",
      back_cut_marks_color: "#ff0000"
    };
    const url = `${config.API_URL}/games/${gameId}/decks`;
    const response = await http.post(url, body);
    return await response.json();
  },

  async updateLayers(deckId, front, layers){
    const body = {"front":front, "layers": layers};
    const url = `${config.API_URL}/decks/${deckId}/layers`;
    const response = await http.post(url, body);
    return await response.json();
  },

  async updateDeck(id, name) {
    const body = {name};
    const url = `${config.API_URL}/decks/${id}`;
    const response = await http.patch(url, body);
    return await response.json();
  },

  forgeDeck(id, printingType, pageSize, fileType) {
    window.open(`${config.API_URL}/decks/${id}/forge_deck?export_target=${printingType}&export_type=${pageSize}&export_format=${fileType}`);
  }
}
