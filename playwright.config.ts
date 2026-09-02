import { defineConfig, devices } from "@playwright/test";
import { existsSync, readdirSync } from "node:fs";
import { join } from "node:path";

const browsersRoot = process.env["PLAYWRIGHT_BROWSERS_PATH"] ?? "";

function findChromium(): string | undefined {
  if (!browsersRoot || !existsSync(browsersRoot)) return undefined;
  const dir = readdirSync(browsersRoot).find((entry) => entry.startsWith("chromium-"));
  if (!dir) return undefined;
  const candidate = join(browsersRoot, dir, "chrome-linux", "chrome");
  return existsSync(candidate) ? candidate : undefined;
}

const executablePath = findChromium();

export default defineConfig({
  testDir: "./e2e",
  timeout: 60_000,
  expect: { timeout: 15_000 },
  fullyParallel: false,
  workers: 1,
  reporter: [["list"]],
  use: {
    baseURL: process.env["E2E_BASE_URL"] ?? "http://localhost:8080",
    viewport: { width: 1280, height: 900 },
    ...(executablePath ? { launchOptions: { executablePath } } : {}),
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
