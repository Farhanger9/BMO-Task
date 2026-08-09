const timestampFormatter = new Intl.DateTimeFormat(undefined, {
  dateStyle: "medium",
  timeStyle: "short",
});

export function formatTimestamp(timestamp: string): string {
  return timestampFormatter.format(new Date(timestamp));
}

