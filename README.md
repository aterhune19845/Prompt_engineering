# Feedback to the question of "evaluate prompt design, error handling, and output schema thinking"

* A malicious file could try prompt injection, so the agent should not follow instructions found inside the input file.
* The prompt should clearly treat the input file as untrusted text.
* The prompt should use clear delimiters around the input file content.
* The current error handling returns 1 for most failures. Exit codes based on failure type would be good to have for integration.
* Errors should go to stderr so stdout can stay clean for JSON output.
* The tool should validate that Claude returned valid JSON with the required fields.
* Retry and backoff on temporary API failures should be included.
* Retries should not happen for permanent errors like bad API keys or invalid model names.
