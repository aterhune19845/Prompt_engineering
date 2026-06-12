# Feedback

* A malicious file could try prompt injection.
* The agent should not follow instructions found inside the input file.
* The current error handling returns 1 for most failures. Exit codes based on failure type would be good to have for integration.
* The current schema may include fields that are not needed. entities, sentiment, and action_items may be not needed.
* Retry on API failure should be included.
