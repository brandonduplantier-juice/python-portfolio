html = open('index.html', 'r', encoding='utf-8').read()

# Find and replace the tags div
old_tags = html[html.find('<div class="tags">'):html.find('</div>', html.find('<div class="tags">'))+6]

new_section = '''<p class="filter-label">Filter by skill</p>
  <div class="tags">
    <span class="tag tag-all" data-filter="all">All Projects</span>
    <span class="tag" data-filter="power-bi">Power BI</span>
    <span class="tag" data-filter="tableau">Tableau</span>
    <span class="tag" data-filter="looker">Looker Studio</span>
    <span class="tag" data-filter="python">Python</span>
    <span class="tag" data-filter="sql">SQL</span>
    <span class="tag" data-filter="ml">Machine Learning</span>
    <span class="tag" data-filter="sheets">Google Sheets</span>
    <span class="tag" data-filter="healthcare">Healthcare</span>
    <span class="tag" data-filter="dax">DAX</span>
  </div>'''

html = html.replace(old_tags, new_section)

# Add data-tags to cards
html = html.replace('href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/Hospital-Readmission-PowerBI"', 'href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/Hospital-Readmission-PowerBI" data-tags="power-bi healthcare dax"')
html = html.replace('href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/HR-Attrition-PowerBI"', 'href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/HR-Attrition-PowerBI" data-tags="power-bi python dax"')
html = html.replace('href="https://public.tableau.com/views/global_happiness_dashboard/GlobalHappinessDashboard2019"', 'href="https://public.tableau.com/views/global_happiness_dashboard/GlobalHappinessDashboard2019" data-tags="tableau python"')
html = html.replace('href="https://datastudio.google.com/reporting/7d8410ea-6d2c-4c91-9f24-ab16f2809e22"', 'href="https://datastudio.google.com/reporting/7d8410ea-6d2c-4c91-9f24-ab16f2809e22" data-tags="looker healthcare sheets"')
html = html.replace('href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/Readmission-Prediction-Model"', 'href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/Readmission-Prediction-Model" data-tags="python ml healthcare"')
html = html.replace('href="https://docs.google.com/spreadsheets/d/15A3XCNeAAntAN3o3DH4Z97v85CsdN2afLzj7Zy2zYhY/edit?usp=sharing"', 'href="https://docs.google.com/spreadsheets/d/15A3XCNeAAntAN3o3DH4Z97v85CsdN2afLzj7Zy2zYhY/edit?usp=sharing" data-tags="sheets healthcare"')
html = html.replace('href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/SQL-Analytics-Portfolio"', 'href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/SQL-Analytics-Portfolio" data-tags="sql"')
html = html.replace('href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/Grammys%20-%20Website%20Analytics%20Project"', 'href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/Grammys%20-%20Website%20Analytics%20Project" data-tags="python"')
html = html.replace('href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/LiveLab"', 'href="https://github.com/brandonduplantier-juice/python-portfolio/tree/main/LiveLab" data-tags="python"')
html = html.replace('href="https://github.com/brandonduplantier-juice/python-portfolio"', 'href="https://github.com/brandonduplantier-juice/python-portfolio" data-tags="python"')

# Add CSS for filter
css_addition = '''
  .tag-all { background: var(--accent); color: #fff; border-color: var(--accent); }
  .tag-all.inactive { background: transparent; color: var(--mid); border-color: var(--rule); }
  .tag { cursor: pointer; transition: all 0.15s ease; user-select: none; }
  .tag:hover { border-color: var(--accent); color: var(--accent); }
  .tag.active { background: var(--accent); color: #fff; border-color: var(--accent); }
  .card.hidden { display: none; }
  .filter-label { font-family: "DM Mono", monospace; font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--mid); margin-bottom: 0.75rem; margin-top: 1.5rem; }
  .no-results { display: none; grid-column: 1 / -1; text-align: center; padding: 3rem; font-family: "DM Mono", monospace; font-size: 0.8rem; color: var(--mid); }'''

html = html.replace('</style>', css_addition + '\n</style>')

# Add JS before closing body
js = '''
<script>
  const tags = document.querySelectorAll(".tag[data-filter]");
  const cards = document.querySelectorAll(".card[data-tags]");
  let active = "all";
  tags.forEach(tag => {
    tag.addEventListener("click", () => {
      active = tag.dataset.filter;
      tags.forEach(t => { t.classList.remove("active"); if(t.dataset.filter==="all") t.classList.add("inactive"); });
      tag.classList.add("active");
      if(tag.dataset.filter==="all") tag.classList.remove("inactive");
      let visible = 0;
      cards.forEach(card => {
        const ct = card.dataset.tags.split(" ");
        if(active==="all" || ct.includes(active)) { card.classList.remove("hidden"); visible++; }
        else card.classList.add("hidden");
      });
    });
  });
</script>'''

html = html.replace('</body>', js + '\n</body>')

open('index.html', 'w', encoding='utf-8').write(html)
print('Done. Length:', len(html))
print('All Projects found:', 'All Projects' in html)
print('filter-label found:', 'filter-label' in html)