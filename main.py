import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found. Make sure it is set in your .env file.")

client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")

    parser.add_argument(
        "user_prompt",
        type=str,
        help="User prompt",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    for i in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
                temperature=0,
            ),
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        function_responses = []

        if response.function_calls:
            for function_call in response.function_calls:
                result = call_function(function_call, args.verbose)

                parts = result.parts

                if not parts:
                    raise RuntimeError("Function call returned no parts")

                fc = parts[0].function_response
                if fc is None or fc.response is None:
                    raise RuntimeError("Invalid function response")

                if args.verbose:
                    print(f"-> {fc.response}")

                function_responses.append(parts[0])

        else:
            print("Final response:")
            print(response.text)
            return

        if function_responses:
            messages.append(
                types.Content(
                    role="user",
                    parts=function_responses,
                )
            )

    print("Agent stopped: max iterations reached.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
