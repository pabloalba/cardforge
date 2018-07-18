import config from '../../../cardforge-config'
import http from './http'

export default {
  retrieveMe: function () {
    return http.fetch('GET', config.API_URL + `/me`)
  },
}
