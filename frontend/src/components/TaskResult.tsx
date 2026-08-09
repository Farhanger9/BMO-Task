import type { TaskExecution } from "../api/tasks";
import { formatTimestamp } from "../formatTimestamp";
import { ExecutionTrace } from "./ExecutionTrace";

interface TaskResultProps {
  execution: TaskExecution;
}

export function TaskResult({ execution }: TaskResultProps) {
  const tools = execution.tools_used.length
    ? execution.tools_used.join(", ")
    : "No tool matched";

  return (
    <section className="panel result-panel" aria-labelledby="current-result-title">
      <div className="section-heading result-heading">
        <div>
          <p className="section-kicker">Latest execution</p>
          <h2 id="current-result-title">Current result</h2>
        </div>
        <time dateTime={execution.timestamp}>
          {formatTimestamp(execution.timestamp)}
        </time>
      </div>

      <div className="result-summary">
        <div className="output-block">
          <span className="metadata-label">Final output</span>
          <p>{execution.output}</p>
        </div>
        <div className="tool-block">
          <span className="metadata-label">Tool used</span>
          <code>{tools}</code>
        </div>
      </div>

      <ExecutionTrace entries={execution.trace} />
    </section>
  );
}

