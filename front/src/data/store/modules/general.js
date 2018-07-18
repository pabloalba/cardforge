import me_api from '../../api/me_api';

export const SET_ME = 'GENERAL_SET_ME';

const state = {
  me: null,
}

const getters = {
  getMe: (state) => state.me,
}

const mutations = {
  [SET_ME] (state, me) {
    state.me = me;
  }
}

const actions = {
  async retrieveMe ({commit}) {
    const me = await me_api.retrieveMe();
    commit(SET_ME, me)
  },
}

export default {
  state,
  getters,
  mutations,
  actions
}
