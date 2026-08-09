export type TraceStage = "received" | "selected" | "executed" | "unsupported";

export interface ExecutionTraceEntry {
  stage: TraceStage;
  message: string;
  tool: string | null;
}

export interface TaskExecution {
  id: number;
  task: string;
  output: string;
  tools_used: string[];
  trace: ExecutionTraceEntry[];
  timestamp: string;
}

export async function runTask(task: string): Promise<TaskExecution> {
  let response: Response;

  try {
    response = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task }),
    });
  } catch {
    throw new Error("Could not reach the task API. Check that the backend is running.");
  }

  if (!response.ok) {
    throw new Error("The task could not be completed. Please try again.");
  }

  return (await response.json()) as TaskExecution;
}

export async function getTaskHistory(
  signal?: AbortSignal,
): Promise<TaskExecution[]> {
  let response: Response;

  try {
    response = await fetch("/api/tasks", { signal });
  } catch (error) {
    if (signal?.aborted) {
      throw error;
    }
    throw new Error("Could not load task history. Check that the backend is running.");
  }

  if (!response.ok) {
    throw new Error("Task history is unavailable right now.");
  }

  return (await response.json()) as TaskExecution[];
}

