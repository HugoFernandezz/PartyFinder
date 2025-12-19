from playwright.sync_api import sync_playwright

def main():
    print("Starting Playwright check...")
    try:
        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.chromium.launch(headless=True)
            print("Browser launched!")
            page = browser.new_page()
            print("Page created!")
            browser.close()
            print("Browser closed. Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
