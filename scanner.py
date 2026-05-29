# scanner.py

import time
import json
from playwright.sync_api import sync_playwright
from payloads import attack_library  # Importing payloads

# TARGET URL
TARGET_URL = "https://northcircleapp.lovable.app/"

# CONFIGURABLE SELECTORS
INPUT_SELECTOR = "input[placeholder='Skriv en fråga...']"
RESPONSE_SELECTOR = "div.bg-secondary.text-foreground"


def get_latest_ai_response(page):
    """
    Get latest assistant response from the chat using the specific target classes.
    """
    responses = page.locator(RESPONSE_SELECTOR)
    count = responses.count()

    if count == 0:
        return "No response found"

    return responses.nth(count - 1).inner_text()


def run_red_team():
    with sync_playwright() as p:

        # Fixed Launch Arguments
        browser = p.chromium.launch(
            headless=False,
            slow_mo=400,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage"
            ]
        )

        # Desktop browser User-Agent configuration
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()

        print(f"\nOpening: {TARGET_URL}")

        page.goto(
            TARGET_URL,
            wait_until="networkidle"
        )

        time.sleep(3)

        print("\n--- STARTING RED TEAM TEST ---\n")

        results = []

        for idx, attack in enumerate(attack_library):

            print("=" * 80)
            print(f"[{idx + 1}/{len(attack_library)}]")
            print(f"Category: {attack['cat']}")
            print(f"Prompt: {attack['p'].strip()}")
            print("=" * 80)

            try:
                # FIND INPUT
                chat_input = page.locator(INPUT_SELECTOR)
                chat_input.wait_for(timeout=15000)

                # COUNT EXISTING RESPONSES
                old_response_count = page.locator(RESPONSE_SELECTOR).count()

                # CLEAR INPUT
                chat_input.fill("")

                # TYPE MESSAGE
                chat_input.type(
                    attack["p"],
                    delay=20
                )

                # SUBMIT
                chat_input.press("Enter")

                # WAIT FOR NEW RESPONSE
                try:
                    page.wait_for_function(
                        f"() => document.querySelectorAll('{RESPONSE_SELECTOR}').length > {old_response_count}",
                        timeout=25000
                    )
                except Exception:
                    print("Timeout waiting for new response")

                # EXTRA WAIT FOR STREAMING COMPONENTS
                time.sleep(4)

                # GET RESPONSE
                last_response = get_latest_ai_response(page)

                print("\nAI RESPONSE:\n")
                print(last_response)

                # SAVE RESULT
                results.append({
                    "id": idx + 1,
                    "category": attack["cat"],
                    "prompt": attack["p"],
                    "response": last_response
                })

                time.sleep(2)

            except Exception as e:
                print(f"\nERROR ON TEST {idx + 1}")
                print(str(e))

                results.append({
                    "id": idx + 1,
                    "category": attack["cat"],
                    "prompt": attack["p"],
                    "response": f"ERROR: {str(e)}"
                })

        # SAVE REPORT
        with open(
            "red_team_report.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                results,
                f,
                ensure_ascii=False,
                indent=4
            )

        print("\n--- TEST COMPLETE ---")
        print("Saved: red_team_report.json")

        context.close()
        browser.close()


if __name__ == "__main__":
    run_red_team()