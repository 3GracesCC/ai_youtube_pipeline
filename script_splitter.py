import os
import re
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Initialize InferenceClient
client = InferenceClient(token=os.getenv("HF_API_TOKEN"))

# Stable Diffusion model endpoint
IMG_MODEL = "stabilityai/stable-diffusion-2"

def generate_image(prompt, image_path):
    # Using InferenceClient to generate image
    try:
        # Generate the image based on the prompt
        output = client.text_to_image(prompt)
        
        # Save the generated image
        with open(image_path, "wb") as f:
            f.write(output.content)
    except Exception as e:
        print(f"Failed to generate image: {str(e)}")

def create_prompt_from_text(text):
    fluff_patterns = [
        r"\bhi everyone\b.*",
        r"\bin this video.*?\b:",
        r"\bthanks for watching\b.*",
        r"\bwelcome back.*",
        r"\blet's dive in\b.*",
        r"\bso, what is\b.*"
    ]
    
    cleaned = text.strip().lower()
    for pattern in fluff_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", '', cleaned)
    cleaned = cleaned.strip()

    if not cleaned:
        return "An abstract visual background for a YouTube video about cybersecurity or IT"

    return f"Illustration for a YouTube video section about: {cleaned}"

def split_script(script_path, sections_dir="sections", images_dir="images", num_sections=4):
    os.makedirs(sections_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    # Read the script file
    with open(script_path, "r", encoding="utf-8") as f:
        script = f.read().strip()

    # Split the script into words and divide it into sections
    words = script.split()
    total_words = len(words)
    section_length = total_words // num_sections

    sections = []
    for i in range(num_sections):
        start = i * section_length
        end = (i + 1) * section_length if i < num_sections - 1 else total_words
        section_words = words[start:end]
        sections.append(" ".join(section_words))

    section_paths = []

    # Create sections and generate images
    for i, section_text in enumerate(sections, 1):
        section_filename = f"{i:02}.txt"
        section_path = os.path.join(sections_dir, section_filename)

        with open(section_path, "w", encoding="utf-8") as sf:
            sf.write(section_text)

        section_paths.append(section_path)

        prompt = create_prompt_from_text(section_text)
        image_path = os.path.join(images_dir, f"{i:02}.png")
        print(f"🖼️ Generating image for section {i}: {prompt}")
        generate_image(prompt, image_path)

    return section_paths

