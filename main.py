import os
from script_generator import generate_script
from script_splitter import split_script

def main():
    topic = input("💡 Enter the topic for your 60-second tech short: ").strip()
    
    print("📝 Generating script...")
    script = generate_script(topic)
    script_path = "script.txt"

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)

    print("✂️ Splitting script and generating images...")
    split_script(script_path)

    print("✅ Workflow complete. Check 'sections/' and 'images/' folders.")

if __name__ == "__main__":
    main()

