import type { TaskExecution } from "../api/tasks";
import { formatTimestamp } from "../formatTimestamp";
import { ExecutionTrace } from "./ExecutionTrace";

interface TaskHistoryProps {
  executions: TaskExecution[];
  isLoading: boolean;
  error: string | null;
}

export function TaskHistory({
  executions,
  isLoading,
  error,
}: TaskHistoryProps) {
  return (
    <section className="history-section" aria-labelledby="history-title">
      <div className="section-heading history-heading">
        <div>
          <p className="section-kicker">Stored executions</p>
          <h2 id="history-title">Task history</h2>
        </div>
        {!isLoading && !error && (
          <span className="history-count">
            {executions.length} {executions.length === 1 ? "task" : "tasks"}
          </span>
        )}
      </div>

      {isLoading && <p className="history-state">Loading task history…</p>}
      {error && (
        <p className="error-message history-error" role="alert">
          {error}
        </p>
      )}
      {!isLoading && !error && executions.length === 0 && (
        <div className="empty-state">
          <h3>No task history yet</h3>
          <p>Your completed task executions will appear here.</p>
        </div>
      )}

      <div className="history-list">
        {executions.map((execution) => {
          const tools = execution.tools_used.length
            ? execution.tools_used.join(", ")
            : "No tool matched";

          return (
            <details key={execution.id} className="history-item">
              <summary>
                <div className="history-summary-main">
                  <span className="metadata-label">Task</span>
                  <strong>{execution.task}</strong>
                  <p>{execution.output}</p>
                </div>
                <div className="history-summary-meta">
                  <code>{tools}</code>
                  <time dateTime={execution.timestamp}>
                    {formatTimestamp(execution.timestamp)}
                  </time>
                  <span className="history-toggle">
                    <span className="history-toggle-open">View trace</span>
                    <span className="history-toggle-close">Hide trace</span>
                  </span>
                </div>
              </summary>
              <div className="history-details">
                <ExecutionTrace entries={execution.trace} />
              </div>
            </details>
          );
        })}
      </div>
    </section>
  );
}
