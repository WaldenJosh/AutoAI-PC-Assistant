import openai
import os

class LLMInterface:
    def __init__(self, api_key=None):
        """
        Initialize the LLMInterface with the OpenAI API key.
        """
        # Set the API key either from the config file or environment variable
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided either as an argument or in the environment variable 'OPENAI_API_KEY'.")

        self.client = openai.Client(api_key=self.api_key)

        # Set the OpenAI API key


        

    def send_prompt(self, prompt, model="gpt-4o-mini"):
        """
        Sends a text prompt to the OpenAI API and returns the response.

        Parameters:
        prompt (str): The input text prompt.
        model (str): The OpenAI model to use (default is 'gpt-3.5-turbo').

        Returns:
        str: The response from the OpenAI API.
        """
        try:
            # Make a request to the OpenAI API with the prompt
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            # Return the content of the response
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error communicating with OpenAI API: {e}")
            return None

if __name__ == "__main__":
    # Test case: Send a "Hello, World!" prompt
    try:
        from config import OPENAI_API_KEY  # Import the API key from config.py
    except ImportError:
        print("API key not found in config.py")
        OPENAI_API_KEY = None

    # Initialize LLMInterface with API key from config.py
    if OPENAI_API_KEY:
        llm_interface = LLMInterface(api_key=OPENAI_API_KEY)

        # Test the LLM with a "Hello, World!" prompt
        test_prompt = "Say Hello World."
        response = llm_interface.send_prompt(test_prompt)

        # Output the result
        if response:
            print("Response from LLM:", response)
        else:
            print("Failed to get response from the LLM.")
    else:
        print("No API key provided.")
