export default {
  fetch: function (method, url) {
    return new Promise((resolve, reject) => {
      fetch(url, {
        method,
        credentials: 'same-origin'
      }).then((response) => {
        if (!response.ok) {
          reject('api error', response.status, response.statusText)
        } else {
          response.json()
            .then((data) => resolve(data))
        }
      })
      .catch((error) => {
        reject(error)
      })
    })
  }
}
