import openai
import os
import base64
import mimetypes


class LLMInterface:
    def __init__(self, api_key=None):
        """
        Initialize the LLMInterface with the OpenAI API key.
        """
        # Set the API key either from the config file or environment variable
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or in the environment variable 'OPENAI_API_KEY'.")

        self.client = openai.Client(api_key=self.api_key)

    def send_prompt(self, prompt, model="gpt-4o-mini"):
        """
        Sends a text prompt to the OpenAI API and returns the response.

        Parameters:
        prompt (str): The input text prompt.
        model (str): The OpenAI model to use.

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

    def send_prompt_with_image(self, prompt, image_path, model="gpt-4o-mini"):
        """
        Sends a text prompt along with an image to the OpenAI API and returns the response.

        Parameters:
        prompt (str): The input text prompt.
        image_path (str): Path to the image file.
        model (str): The OpenAI model to use.

        Returns:
        str: The response from the OpenAI API.
        """
        try:
            # Determine the MIME type of the image
            img_type, _ = mimetypes.guess_type(image_path)
            if not img_type:
                raise ValueError(
                    f"Could not determine the MIME type of the image: {image_path}")

            # Open the image file and base64 encode it
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(
                    image_file.read()).decode("utf-8")

            # Prepare the prompt with the image as a base64 URL
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:{img_type};base64,{encoded_image}"},
                            },
                        ],
                    }
                ],
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

        # Test sending an image with a prompt
        image_path = "test_image.png"  # Replace this with the actual image path
        test_prompt_with_image = "Given the current screen, please describe the steps needed to open Windows setting and get to Windows Update. Describe this using only the keyboard as input."
        response_with_image = llm_interface.send_prompt_with_image(
            test_prompt_with_image, image_path)

        # Output the result
        if response_with_image:
            print("Response from LLM (with image):", response_with_image)
        else:
            print("Failed to get response from the LLM (with image).")
    else:
        print("No API key provided.")
