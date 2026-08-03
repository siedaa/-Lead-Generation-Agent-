from dotenv import load_dotenv
from agent.pipeline import run_pipeline


def main():
    load_dotenv()
    print("=" * 50)
    print("  LeadGenAgent - AI Lead Generation Tool")
    print("=" * 50)
    user_prompt = input("\nDescribe the leads you're looking for (e.g. 'coffee shops in Karachi'): ").strip()

    if not user_prompt:
        print("No input provided. Exiting.")
        return

    print("\nSearching... this may take 30-60 seconds.\n")
    result = run_pipeline(user_prompt, headless=False)

    if result["error"]:
        print(f"\n{result['error']}")
        return

    print("=" * 50)
    print("  SUMMARY")
    print("=" * 50)
    print(f"  Search query : {result['query']}")
    print(f"  Leads found  : {len(result['leads'])}")
    print(f"  Saved to     : {result['filepath']}")
    print("=" * 50)


if __name__ == "__main__":
    main()
