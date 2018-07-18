import Vue from 'vue';
import Vuex from 'vuex';

import meApi from '../api/me_api';

export const SET_ME = 'GENERAL_SET_ME';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    me: null,
  },

  mutations: {
    [SET_ME] (state, me) {
      state.me = me;
    }
  },

  actions: {
    async retrieveMe ({commit}) {
      const me = await meApi.retrieveMe();
      commit(SET_ME, me)
    },
  }
})
