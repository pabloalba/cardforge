import config from '../../../cardforge-config'
import http from './http'

export default {
  retrieveMe() {
    return http.fetch('GET', `${config.API_URL}/me`);
  },
  retrieveGames() {
    return http.fetch('GET', `${config.API_URL}/me`);
  }
}
