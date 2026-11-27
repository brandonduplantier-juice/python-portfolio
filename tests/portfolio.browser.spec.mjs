import { test, expect } from '@playwright/test';

for (const viewport of [{width:1440,height:900},{width:390,height:844}]) {
  test('portfolio navigation and filters at '+viewport.width+'px', async ({page}) => {
    await page.setViewportSize(viewport);
    await page.emulateMedia({reducedMotion:'reduce'});
    const errors=[];
    page.on('pageerror', error=>errors.push(error.message));
    await page.goto('http://127.0.0.1:8765/index.html');
    const cards=page.locator('.card[data-tags]');
    const visible=page.locator('.card[data-tags]:visible');
    const filters=page.locator('button[data-filter]');
    await expect(cards).toHaveCount(23);
    await expect(visible).toHaveCount(23);
    await expect(filters).toHaveCount(14);
    for(const button of await filters.all()){
      const filter=await button.getAttribute('data-filter');
      const expected=await cards.evaluateAll((nodes,f)=>nodes.filter(n=>f==='all'||n.dataset.tags.split(' ').includes(f)).length,filter);
      await button.focus();
      await page.keyboard.press('Enter');
      await expect(button).toHaveAttribute('aria-pressed','true');
      await expect(visible).toHaveCount(expected);
      await expect(page.locator('#filter-status')).toHaveText('Showing '+expected+' of 23 projects');
      for(const zone of await page.locator('.zone').all()){
        const count=await zone.locator('.card:not(.hidden)').count();
        if(count) await expect(zone).toBeVisible(); else await expect(zone).toBeHidden();
      }
    }
    await page.locator('.portfolio-nav a[href="#engineering"]').click();
    await expect(visible).toHaveCount(23);
    await expect(page.locator('#engineering')).toBeVisible();
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1)).toBeTruthy();
    expect(errors).toEqual([]);
  });
}
