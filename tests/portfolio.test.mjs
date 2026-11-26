import { readFileSync, existsSync } from 'node:fs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { runInNewContext } from 'node:vm';

const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const ids = [...html.matchAll(/<div class="zone" id="([^"]+)"/g)].map(m => m[1]);
const sections = html.split(/<div class="zone" id="[^"]+">/).slice(1);
const make = (dataset={}) => {
  const classes = new Set(), attrs = {}, events = {};
  return {dataset, attrs, events, classList:{toggle(k,v){v?classes.add(k):classes.delete(k)}, contains(k){return classes.has(k)}}, setAttribute(k,v){attrs[k]=v}, addEventListener(k,fn){events[k]=fn}};
};
const zones = sections.map(section => {
  const cards = [...section.matchAll(/class="card[^"]*"[^>]*data-tags="([^"]+)"/g)].map(m=>make({tags:m[1]}));
  return {...make(),cards,querySelector(){return cards.find(c=>!c.classList.contains('hidden'))}};
});
const cards = zones.flatMap(z=>z.cards);
const tags = [...html.matchAll(/<button type="button" class="tag[^"]*" data-filter="([^"]+)"/g)].map(m=>make({filter:m[1]}));
const links = [...html.matchAll(/<nav class="portfolio-nav"[^>]*>(.*?)<\/nav>/gs)].flatMap(m=>[...m[1].matchAll(/href="#([^"]+)"/g)]).map(m=>make({target:m[1]}));
const status = {};
const doc = {querySelectorAll(s){return {'.tag[data-filter]':tags,'.card[data-tags]':cards,'.zone':zones,'.portfolio-nav a':links}[s]},getElementById(){return status}};
const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].at(-1)[1];
test('all project cards, sections and local links exist',()=>{
  assert.equal(cards.length,23); assert.equal(tags.length,14);
  assert.deepEqual(ids,['engineering','development','research','client-work','foundations']);
  assert.deepEqual(links.map(x=>x.dataset.target),ids);
  for(const [,href] of html.matchAll(/href="([^"]+)"/g)){
    if (/^(https?:|mailto:|#)/.test(href)) continue;
    assert.ok(existsSync(new URL('../'+href,import.meta.url)),href);
  }
});
test('actual filter script updates cards, sections, pressed state and counts',()=>{
  runInNewContext(script,{document:doc});
  for(const tag of tags){
    tag.events.click();
    const filter=tag.dataset.filter;
    const expected=cards.filter(c=>filter==='all'||c.dataset.tags.split(' ').includes(filter));
    assert.deepEqual(cards.filter(c=>!c.classList.contains('hidden')),expected);
    assert.equal(status.textContent,`Showing ${expected.length} of ${cards.length} projects`);
    for(const t of tags)assert.equal(t.attrs['aria-pressed'],String(t===tag));
    for(const z of zones)assert.equal(z.classList.contains('hidden'),!z.cards.some(c=>expected.includes(c)));
  }
  links[0].events.click();
  assert.equal(cards.filter(c=>!c.classList.contains('hidden')).length,23);
});
