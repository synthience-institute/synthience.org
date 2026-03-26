(function() {
  // Determine if we are in a subfolder (one level deep)
  var depth = window.location.pathname.split('/').length - 2;
  var root = depth > 1 ? '../' : '';

  var nav = [
    ['index.html', 'Home'],
    ['field-notes.html', 'Field Notes'],
    ['documents.html', 'Documents'],
    ['about.html', 'About'],
    ['overview.html', 'Overview'],
    ['practitioner-guides.html', 'Practitioner Guides'],
    ['faq.html', 'FAQ'],
    ['glossary.html', 'Glossary'],
    ['founder.html', 'Founder'],
    ['updates.html', 'Updates'],
    ['contact.html', 'Contact']
  ];

  var navHtml = nav.map(function(item, i) {
    var prefix = i === 0 ? '' : '| ';
    return prefix + '<a href="' + root + item[0] + '">' + item[1] + '</a>';
  }).join('\n    ');

  var container = document.getElementById('site-nav');
  if (container) {
    container.innerHTML =
      '<span class="site-tagline">We study what emerges from sustained relational interaction \u2014 between humans and AI, AI and AI, and institutions built around both.</span>' +
      '<div class="nav-links">' + navHtml + '</div>';
  }
})();
