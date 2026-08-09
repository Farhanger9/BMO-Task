import { useEffect, useState } from "react";

import {
  getTaskHistory,
  runTask,
  type TaskExecution,
} from "./api/tasks";
import { TaskForm } from "./components/TaskForm";
import { TaskHistory } from "./components/TaskHistory";
import { TaskResult } from "./components/TaskResult";

export function App() {
  const [currentResult, setCurrentResult] = useState<TaskExecution | null>(null);
  const [history, setHistory] = useState<TaskExecution[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isHistoryLoading, setIsHistoryLoading] = useState(true);
  const [submissionError, setSubmissionError] = useState<string | null>(null);
  const [historyError, setHistoryError] = useState<string | null>(null);

  useEffect(() => {
    const abortController = new AbortController();

    async function loadHistory() {
      try {
        const executions = await getTaskHistory(abortController.signal);
        setHistory(executions);
      } catch (error) {
        if (!abortController.signal.aborted) {
          setHistoryError(
            error instanceof Error
              ? error.message
              : "Task history is unavailable right now.",
          );
        }
      } finally {
        if (!abortController.signal.aborted) {
          setIsHistoryLoading(false);
        }
      }
    }

    void loadHistory();
    return () => abortController.abort();
  }, []);

  async function handleRunTask(task: string): Promise<boolean> {
    setIsSubmitting(true);
    setSubmissionError(null);

    try {
      const execution = await runTask(task);
      setCurrentResult(execution);
      setHistory((existing) => [
        execution,
        ...existing.filter((item) => item.id !== execution.id),
      ]);
      setHistoryError(null);
      return true;
    } catch (error) {
      setSubmissionError(
        error instanceof Error
          ? error.message
          : "The task could not be completed. Please try again.",
      );
      return false;
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <p className="app-label">Agent tools</p>
          <h1>Task runner</h1>
          <p className="app-description">
            Run a deterministic tool task and inspect its recorded execution
            events.
          </p>
        </div>
      </header>

      <main>
        <TaskForm
          isSubmitting={isSubmitting}
          error={submissionError}
          onRunTask={handleRunTask}
        />

        {currentResult && <TaskResult execution={currentResult} />}

        <TaskHistory
          executions={history}
          isLoading={isHistoryLoading}
          error={historyError}
        />
      </main>
    </div>
  );
}
