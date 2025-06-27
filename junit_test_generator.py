import os

try:
    import openai
except ImportError:  # pragma: no cover - openai may not be installed in tests
    openai = None

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
    if not openai:
        # In test environments openai might not be installed
        return {"junit_test": ""}

    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert Java test writer."},
            {"role": "user", "content": state["prompt"]},
        ],
        max_tokens=800,
    )
    junit_test = response.choices[0].message.content.strip()
    return {"junit_test": junit_test}


def generate_junit_test(java_method_code):
    if StateGraph is None:
        # Fallback when langgraph is unavailable
        return _call_llm(_craft_prompt({"method": java_method_code}))[
            "junit_test"
        ]

    sg = StateGraph()
    sg.add_node("prompt", _craft_prompt)
    sg.add_node("llm", _call_llm)
    sg.add_edge("prompt", "llm")
    sg.set_entry_point("prompt")
    result = sg.invoke({"method": java_method_code})
    return result["junit_test"]


if __name__ == "__main__":
    from extract_method import extract_method
    method_code = extract_method('HelloWorld.java')
    print("Extracted Method:\n", method_code)
    junit_test = generate_junit_test(method_code)
    print("\nGenerated JUnit Test:\n", junit_test)
