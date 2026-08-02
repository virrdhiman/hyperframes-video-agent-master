const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const articles = [
  {
    id: "atlassian",
    source: "TECHCRUNCH",
    date: "Mar 12",
    title: "Atlassian cuts 10% of workforce as it pivots heavily to AI",
    subtitle: "The collaboration software giant says it needs to rebalance its resources towards artificial intelligence.",
    author: "Ron Miller"
  },
  {
    id: "amazon",
    source: "WSJ",
    date: "Jan 18",
    title: "Amazon Lays Off 16,000 Employees Amid Push for Efficiency",
    subtitle: "The ecommerce giant cites overhiring and macroeconomic conditions, but insists output remains the same.",
    author: "Dana Mattioli"
  },
  {
    id: "block",
    source: "CNBC",
    date: "Feb 05",
    title: "Block slashes 40% of workforce, Jack Dorsey cites AI productivity gains",
    subtitle: "The fintech firm says AI models are doing the internal work of entire engineering teams.",
    author: "Ashley Capoot"
  },
  {
    id: "meta",
    source: "THE VERGE",
    date: "Nov 30",
    title: "Meta planning 'more layoffs' while spending $100 Billion on AI",
    subtitle: "Mark Zuckerberg warns employees that another round of restructuring is imminent to fund the AI war.",
    author: "Alex Heath"
  }
];

const htmlTemplate = (article) => `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #FFF; padding: 40px; margin: 0; color: #111; }
    .news-container { max-width: 800px; margin: 0 auto; border-bottom: 2px solid #EAEAEA; padding-bottom: 30px; }
    .source { font-weight: 800; color: #E53935; font-size: 14px; letter-spacing: 2px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; text-transform: uppercase; }
    .title { font-size: 48px; font-weight: 900; line-height: 1.1; margin: 10px 0 20px; letter-spacing: -1px; }
    .subtitle { font-size: 24px; color: #555; line-height: 1.4; font-weight: 400; margin-bottom: 25px; }
    .meta { display: flex; align-items: center; gap: 15px; font-size: 16px; color: #777; font-weight: 500; }
    .author { font-weight: 700; color: #000; }
    .divider { width: 100%; height: 1px; background: #CCC; margin: 20px 0; }
  </style>
</head>
<body>
  <div class="news-container" id="capture-zone">
    <div class="source"><span>${article.source}</span> <span>${article.date}</span></div>
    <div class="title">${article.title}</div>
    <div class="subtitle">${article.subtitle}</div>
    <div class="meta">
      By <span class="author">${article.author}</span>
    </div>
    <div class="divider"></div>
  </div>
</body>
</html>
`;

async function main() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 900, height: 600, deviceScaleFactor: 2 });
  
  const destDir = path.join(__dirname, '..', 'public', 'news-screenshots');
  if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });

  for (const article of articles) {
    const html = htmlTemplate(article);
    await page.setContent(html);
    const element = await page.$('#capture-zone');
    const outputPath = path.join(destDir, `${article.id}.png`);
    await element.screenshot({ path: outputPath });
    console.log(`Captured ${outputPath}`);
  }

  await browser.close();
}

main().catch(console.error);
