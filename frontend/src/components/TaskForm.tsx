import { useState, type FormEvent, type KeyboardEvent } from "react";

interface TaskFormProps {
  isSubmitting: boolean;
  error: string | null;
  onRunTask: (task: string) => Promise<boolean>;
}

export function TaskForm({
  isSubmitting,
  error,
  onRunTask,
}: TaskFormProps) {
  const [task, setTask] = useState("");
  const canSubmit = task.trim().length > 0 && !isSubmitting;

  async function submitTask() {
    if (!canSubmit) {
      return;
    }

    const succeeded = await onRunTask(task.trim());
    if (succeeded) {
      setTask("");
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void submitTask();
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (
      event.key === "Enter" &&
      !event.shiftKey &&
      !event.nativeEvent.isComposing
    ) {
      event.preventDefault();
      void submitTask();
    }
  }

  return (
    <section className="panel" aria-labelledby="task-form-title">
      <div className="section-heading">
        <div>
          <p className="section-kicker">New execution</p>
          <h2 id="task-form-title">Run a task</h2>
        </div>
        <span className="keyboard-hint">Enter to run · Shift+Enter for a line break</span>
      </div>

      <form onSubmit={handleSubmit}>
        <label htmlFor="task-input">Task</label>
        <textarea
          id="task-input"
          value={task}
          onChange={(event) => setTask(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Example: uppercase: deployment ready"
          rows={4}
          disabled={isSubmitting}
          aria-describedby="task-help"
        />
        <div className="form-footer">
          <p id="task-help" className="field-help">
            Try a text operation, arithmetic expression, or weather request.
          </p>
          <button type="submit" disabled={!canSubmit}>
            {isSubmitting ? "Running task…" : "Run task"}
          </button>
        </div>
        {error && (
          <p className="error-message" role="alert">
            {error}
          </p>
        )}
      </form>
    </section>
  );
}
