const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    // Listen for console logs from the browser
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));

    // Go to the local game project homepage
    await page.goto('http://localhost:8080/', { waitUntil: 'networkidle0', timeout: 30000 });

    // Wait for the loader to finish and the content to become visible
    try {
        await page.waitForFunction(() => {
            const loader = document.querySelector('.loader');
            return !loader || window.getComputedStyle(loader).display === 'none' || window.getComputedStyle(loader).opacity === '0';
        }, { timeout: 15000 });
        console.log("Loader finished.");

        // Let animations settle
        await new Promise(r => setTimeout(r, 2000));

        // Take a screenshot of the homepage
        const screenshotPath = 'C:/Users/Serkan/.gemini/antigravity/brain/d94f4472-def5-4286-8578-ebd3d80b8aae/homepage_categories_verification.png';
        await page.screenshot({ path: screenshotPath });
        console.log(`Saved screenshot to ${screenshotPath}`);

        // Extract inner text of the category links
        const linksData = await page.evaluate(() => {
            const links = Array.from(document.querySelectorAll('.link_galerie'));
            return links.map(el => ({
                href: el.getAttribute('href'),
                text: el.innerText.trim() || el.textContent.trim()
            }));
        });
        console.log("Category Links Data:", linksData);

    } catch (e) {
        console.log("Error waiting for content:", e);
    }

    await browser.close();
})();
