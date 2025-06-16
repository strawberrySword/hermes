from main import run_fetcher


if __name__ == "__main__":
    try:
        run_fetcher()
        print("news fetch completed successfully.")
    except Exception as e:
        print(f"Error during fetch: {e}")


