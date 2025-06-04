
# openai.api_key = "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"  # Replace with your API key
import openai
from extract_method import extract_method

openai.api_key = "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"  # Replace with your API key

def generate_junit_test(java_method_code):
    prompt = f"""
You are a senior Java developer. Write a JUnit 5 test for the following Java method. 
Include parameterized tests and mocking (use Mockito) if needed.

Method code:
{java_method_code}
    """

    # The new OpenAI API syntax (for >=1.0.0)
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-4o",  # or gpt-4, gpt-4-1 if you have access
        messages=[
            {"role": "system", "content": "You are an expert Java test writer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800
    )
    junit_test = response.choices[0].message.content
    return junit_test.strip()

if __name__ == "__main__":
    method_code = extract_method('HelloWorld.java')
    print("Extracted Method:\n", method_code)
    junit_test = generate_junit_test(method_code)
    print("\nGenerated JUnit Test:\n", junit_test)
