import {isPlainObject} from "lodash";
import Cookies from "js-cookie";

const defaultOptions = {
  credentials: 'include',
  mode: 'cors',
  redirect: 'follow',
  referer: 'no-referer',
}

export default {
  request({method, url, body, headers={}, opts}) {
    headers = Object.assign({
      "X-CSRFToken": Cookies.get('csrftoken')
    }, headers);

    const options = Object.assign({}, defaultOptions, opts, {
      method: method.toUpperCase(),
      headers: headers,
      body: body
    });

    if (isPlainObject(body)) {
      options.body = JSON.stringify(body);
      options.headers["content-type"] = "application/json";
    }

    return fetch(url, options);
    // .then(async (response) => {
    //       const status = response.status;
    //       const headers = {};

    //       for (let key of response.headers.keys()) {
    //         headers[key.toLowerCase()] = response.headers.get(key);
    //       }

    //       const result = {
    //         status: status,
    //         headers: headers,
    //       };

    //       const contentType = headers["content-type"] || "";
    //       if (contentType.startsWith("application/json")) {
    //         result.body = await response.json();
    //       } else if (contentType.startsWith("text/")) {
    //         result.body = await response.text();
    //       } else {
    //         result.body = await response.blob();
    //       }

    //       return result;
    //     });
  },

  get(url, options) {
    return this.request({method:"get", url:url, params: options});
  },

  getJSON(url, options) {
    return this.get(url, options).then((rsp) => rsp.json());
  },

  post(url, body, options) {
    options = Object.assign({url: url, method: "POST", body: body}, options);
    return this.request(options);
  },

  put(url, body, options) {
    options = Object.assign({url: url, method: "PUT", body: body}, options);
    return this.request(options);
  },

  patch(url, body, options) {
    options = Object.assign({url: url, method: "PATCH", body: body}, options);
    return this.request(options);
  }
}
