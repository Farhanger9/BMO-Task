import type { ExecutionTraceEntry, TraceStage } from "../api/tasks";

interface ExecutionTraceProps {
  entries: ExecutionTraceEntry[];
}

const stageLabels: Record<TraceStage, string> = {
  received: "Task received",
  selected: "Tool selected",
  executed: "Tool executed",
  unsupported: "Request unsupported",
};

export function ExecutionTrace({ entries }: ExecutionTraceProps) {
  return (
    <div className="execution-trace">
      <div className="trace-heading">
        <h3>Execution events</h3>
        <span>{entries.length} steps</span>
      </div>
      <ol className="trace-list">
        {entries.map((entry, index) => (
          <li key={`${entry.stage}-${index}`} className="trace-item">
            <div className="trace-marker" aria-hidden="true">
              {index + 1}
            </div>
            <div className="trace-content">
              <div className="trace-step-heading">
                <span>{stageLabels[entry.stage]}</span>
                {entry.tool && <code>{entry.tool}</code>}
              </div>
              <p>{entry.message}</p>
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
}

