import { defineConfig, defaultExclude } from "vitest/config";
import viteConfig from "./vite.config";

export default defineConfig(async (env) => {
  const base = typeof viteConfig === "function" ? await viteConfig(env) : viteConfig;
  return {
    ...base,
    test: {
      ...(base.test ?? {}),
      exclude: [...defaultExclude, "e2e/**"],
    },
  };
});
