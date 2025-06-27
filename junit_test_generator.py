import os

try:
    import openai
except ImportError:  # pragma: no cover - openai may not be installed in tests
    openai = None

try:
    from langchain.chat_models import ChatOpenAI
except Exception:  # pragma: no cover - langchain may not be installed in tests
    ChatOpenAI = None

try:
    from langsmith import traceable
except Exception:  # pragma: no cover - langsmith may not be installed

    def traceable(func=None, **kwargs):
        if func is None:

            def wrapper(f):
                return f

            return wrapper
        return func


try:
    from langgraph.graph import StateGraph
except Exception:  # pragma: no cover - langgraph may not be installed in tests
    StateGraph = None

# Read the API key from the environment to avoid hard coding secrets
if openai:
    openai.api_key = os.getenv("OPENAI_API_KEY", "")


def _craft_prompt(state):
    method = state["method"]
    prompt = f"""You are a senior Java developer. Write a JUnit 5 test for the following Java method.
Include parameterized tests and mocking (use Mockito) if needed.

Method code:
{method}
"""
    return {"prompt": prompt}


def _call_llm(state):
    prompt = state["prompt"]

    if ChatOpenAI is not None:
        llm = ChatOpenAI(model_name="gpt-4o", max_tokens=800)

        @traceable
        def run(prompt_text: str) -> str:
            result = llm.invoke(prompt_text)
            return result.content.strip()

        junit_test = run(prompt)
        return {"junit_test": junit_test}

    if openai is not None:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert Java test writer."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
        )
        junit_test = response.choices[0].message.content.strip()
        return {"junit_test": junit_test}

    # No LLM backend available
    return {"junit_test": ""}


def generate_junit_test(java_method_code):
    if StateGraph is None:
        # Fallback when langgraph is unavailable
        return _call_llm(_craft_prompt({"method": java_method_code}))["junit_test"]

    sg = StateGraph()
    sg.add_node("prompt", _craft_prompt)
    sg.add_node("llm", _call_llm)
    sg.add_edge("prompt", "llm")
    sg.set_entry_point("prompt")
    result = sg.invoke({"method": java_method_code})
    return result["junit_test"]


if __name__ == "__main__":
    from extract_method import extract_method

    method_code = extract_method("HelloWorld.java")
    print("Extracted Method:\n", method_code)
    junit_test = generate_junit_test(method_code)
    print("\nGenerated JUnit Test:\n", junit_test)
