import { defineConfig } from "@playwright/test";

const backendPython =
  process.platform === "win32"
    ? "../backend/.venv/Scripts/python.exe"
    : "../backend/.venv/bin/python";

export default defineConfig({
  testDir: "./e2e",
  workers: 1,
  use: {
    baseURL: "http://127.0.0.1:5173",
    trace: "retain-on-failure",
  },
  webServer: [
    {
      command: `${backendPython} -m uvicorn app.main:app --app-dir ../backend --port 8000`,
      url: "http://127.0.0.1:8000/api/tasks",
      env: {
        TASK_DATABASE_PATH: "../backend/playwright.sqlite3",
      },
      reuseExistingServer: true,
    },
    {
      command: "npm run dev -- --host 127.0.0.1",
      url: "http://127.0.0.1:5173",
      reuseExistingServer: true,
    },
  ],
});
