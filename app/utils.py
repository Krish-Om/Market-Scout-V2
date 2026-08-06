import functools

run_metrics = []


# Input (Prompt) Rate: $\$0.075$ per 1,000,000 tokens
# Output (Completion) Rate: $\$0.300$ per 1,000,000 tokens
def track_tokens(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        raw_response = await func(*args, **kwargs)

        usage = raw_response.usage
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens

        cost = (prompt_tokens / 1_000_000 * 0.075) + (
            completion_tokens / 1_000_000 * 0.300
        )
        run_metrics.append(
            {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "cost_usd": cost,
            }
        )
        return raw_response.choices[0].message.content

    return wrapper
