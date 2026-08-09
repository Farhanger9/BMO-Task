import { expect, test } from "@playwright/test";

test("runs a calculator task and records it in history", async ({ page }) => {
  await page.goto("/");

  const taskInput = page.getByRole("textbox", { name: "Task" });
  await taskInput.fill("25 * 8");
  await page.getByRole("button", { name: "Run task" }).click();

  const currentResult = page.getByRole("region", { name: "Current result" });
  await expect(currentResult.getByText("200", { exact: true })).toBeVisible();
  await expect(
    currentResult.getByText("calculator", { exact: true }).first(),
  ).toBeVisible();

  const history = page.getByRole("region", { name: "Task history" });
  await expect(history.getByText("25 * 8", { exact: true }).first()).toBeVisible();
});

test("keeps the UI usable after an unsupported task", async ({ page }) => {
  await page.goto("/");

  const taskInput = page.getByRole("textbox", { name: "Task" });
  const runButton = page.getByRole("button", { name: "Run task" });

  await taskInput.fill("book me a flight to Vancouver");
  await runButton.click();

  const currentResult = page.getByRole("region", { name: "Current result" });
  await expect(
    currentResult.getByText("Unsupported task.", { exact: true }),
  ).toBeVisible();
  await expect(taskInput).toBeEnabled();

  await taskInput.fill("1 + 1");
  await expect(runButton).toBeEnabled();
});

