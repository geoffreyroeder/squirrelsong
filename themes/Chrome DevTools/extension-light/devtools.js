/* global chrome */

// eslint-disable-next-line unicorn/prefer-top-level-await
fetch(chrome.runtime.getURL('devtools.css')).then((response) => {
  response.text().then((text) => {
    chrome.devtools.panels.applyStyleSheet(text);
  });
});
