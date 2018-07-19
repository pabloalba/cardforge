import {isPlainObject} from "lodash";
import Cookies from "js-cookie";
import store from "../store";

const defaultOptions = {
  credentials: 'include',
  mode: 'cors',
  redirect: 'follow',
  referer: 'no-referer',
}

export class HttpError extends Error {
  constructor(response) {
    if (isPlainObject(response.body) && response.body.detail) {
      super(response.body.detail);
    } else {
      super("Http Error");
    }

    this.status = response.status;
    this.response = response;
  }
}

export class Response {
  constructor(status, body, response) {
    this.body = body;
    this.status = status;
    this.headers = parseHeaders(response);

    this.__response = response;

    Object.freeze(this.headers);
  }
}

function conditionalBodyDecode(response) {
  const contentType = response.headers["content-type"] || "";
  if (contentType.startsWith("application/json")) {
    response.body = JSON.parse(response.body);
    response.isBodyJson = true;
  }
  return response;
}

function raiseOnHttpError(response) {
  if (response.status >= 200 && response.status <= 299) {
    return response;
  } else {
    throw new HttpError(response);
  }
}

function handleError(error) {
  if (error instanceof HttpError) {
    store.dispatch("handleError", error);
  }
  return error;
}

function parseHeaders(response) {
  const headers = {};
  for (let key of response.headers.keys()) {
    headers[key.toLowerCase()] = response.headers.get(key);
  }
  return headers;
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

    return fetch(url, options)
      .then(async (response) => {
        const body = await response.text();
        const status = response.status;
        return new Response(status, body, response);
      })
      .then(conditionalBodyDecode)
      .then(raiseOnHttpError)
      .catch(handleError);
  },

  get(url, options) {
    return this.request({method:"get", url:url, params: options});
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
  },

  delete(url, options) {
    options = Object.assign({url: url, method: "DELETE"}, options);
    return this.request(options);
  }
}
