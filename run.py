import subprocess
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <module_name>")
        print("Example: python run.py github_code")
        sys.exit(1)
    
    module_name = sys.argv[1]
    result = subprocess.run(
        ["uv", "run", "python", "-m", f"{module_name}.main"]
    )
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
