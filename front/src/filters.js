import { format } from "date-fns";

export default {
  install(Vue, options) {
    Vue.filter("format", function (value, fmt) {
      return format(value, fmt);
    });
  }
};
