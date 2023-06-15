
const config = {
  API_URL: '',

  USERNAME: 'admin',
  PASSWORD: 'admin',
};

// [Note]
//  React's process.env is passed (configured) from npm's process.env by /config/env.js,
//  which only works when running on npm server (dev/testing purpose).
if (process.env.NODE_ENV === 'test') {
  config.API_URL = `http://localhost:${process.env.PORT}/api`;
} else {
  config.API_URL = process.env.REACT_APP_HTTP_API_URL ? process.env.REACT_APP_HTTP_API_URL : "/api";
}

// config.API_URL = "http://172.31.64.244:8080"
// config.API_URL = "http://0:8080"
// config.API_URL = "http://1.1.1.1:8080"
// config.API_URL = "http://0.0.0.0:8080"
config.API_URL = "http://127.0.0.1:8080"
// config.API_URL = "GGGGGGGGGGGGGGGGGGGGGG"
// config.API_URL = "http://127.0.0.1:443"
export default config;
