import { readdir, readFile, writeFile } from "node:fs/promises";
import { extname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const marker = '<script defer src="/analytics.js"></script>';
let changed = 0;
let inspected = 0;

async function walk(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (entry.name === ".git" || entry.name === "node_modules") continue;
    const path = join(directory, entry.name);
    if (entry.isDirectory()) {
      await walk(path);
      continue;
    }
    if (extname(entry.name).toLowerCase() !== ".html") continue;

    inspected += 1;
    const html = await readFile(path, "utf8");
    if (html.includes(marker) || !html.includes("</head>")) continue;
    await writeFile(path, html.replace("</head>", `${marker}\n</head>`), "utf8");
    changed += 1;
  }
}

await walk(root);
console.log(`analytics injection complete: ${changed} changed, ${inspected} inspected`);
