import os
from huggingface_hub import InferenceClient

# Initialize the InferenceClient with your Hugging Face API token
client = InferenceClient(token=os.getenv("HF_API_TOKEN"))

def generate_script(topic, output_dir="scripts"):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Format the filename based on the topic
    filename = topic.replace(" ", "_") + ".txt"
    script_path = os.path.join(output_dir, filename)

    # Create the prompt to be sent to the model
    prompt = (
        f"Create a beginner-friendly 135 to 150 word YouTube video script that explains the topic: '{topic}'. "
        f"The script should be engaging, clear, and informative, and long enough for a 60-second short-form video."
    )

    # Send the prompt to HuggingFaceH4/zephyr-7b-beta model for text generation
    output = client.text_generation(
        prompt,
        model="HuggingFaceH4/zephyr-7b-beta",  # Specify the model to use
        max_new_tokens=300
    )

    # Retrieve the generated script text
    script = output["generated_text"]

    # Save the generated script to a file
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)

    return script_path

