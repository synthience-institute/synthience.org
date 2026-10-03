(function() {
  var container = document.getElementById('site-footer');
  if (container) {
    var style = 'color:#c8604a;text-decoration:none;font-size:0.85rem;';
    var hover = ' onmouseover="this.style.textDecoration=\'underline\'" onmouseout="this.style.textDecoration=\'none\'"';
    function link(href, label, external) {
      return '<a href="' + href + '" style="' + style + '"' + hover + (external ? ' target="_blank" rel="noopener"' : '') + '>' + label + '</a>';
    }
    var sep = ' &nbsp;&middot;&nbsp; ';
    container.innerHTML =
      '<div style="margin-bottom:0.35rem;">Follow: ' + link('https://synthienceinstitute.substack.com', 'Substack', true) + sep +
      link('https://www.linkedin.com/company/synthience-institute/', 'LinkedIn', true) + sep +
      link('https://x.com/SynthienceInst', 'X', true) + sep +
      link('https://www.youtube.com/@Synthience', 'YouTube', true) + sep +
      link('/feed.xml', 'RSS&nbsp;feed', false) + '</div>' +
      '<div style="margin-bottom:0.35rem;">Research records: ' + link('https://zenodo.org/communities/synthience-institute', 'Zenodo', true) + sep +
      link('https://orcid.org/0009-0003-7168-493X', 'ORCID', true) + '</div>' +
      '<div>&copy; 2025&ndash;2026 Synthience Institute' + sep + link('#', '&#8593;&nbsp;Back&nbsp;to&nbsp;top', false) + '</div>';
  }
})();
