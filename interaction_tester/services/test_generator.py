import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

def get_prompt_template(website_type):
    templates = {
        'ecommerce': """
           
            You are an expert QA engineer. Generate a complete and well-structured Selenium test script in Python to test the website: `{url}`.

            Requirements:

            1. Open the browser (Chrome WebDriver) visibly during test execution — do not run in headless mode.
            2. Verify that the base URL loads successfully without errors.
            3. Highlight every interacted element with a 1px solid red border for visual debugging.
            4. Wait for 0.5 seconds after each interaction to simulate natural user behavior.
            5. Perform smooth scrolling up and down the page to ensure all dynamic elements are triggered.
            6. Test a valid login flow using `standard_user` and `secret_sauce` (or appropriate credentials for the site).
            7. Interact with key UI elements:
                * Clickable buttons (e.g., "Add to cart")
                * Dropdowns (e.g., sorting dropdowns)
                * Navigation links (e.g., sidebar, About, Logout)
            8. Highlight and interact with all visible inventory or content items, where applicable.
            9. Simulate tests on three screen sizes:
                * Desktop: 1920x1080
                * Tablet: 768x1024
                * Mobile: 375x667
            10. Ensure that the layout and responsiveness are correct for all screen sizes tested.
            11. After each test, log results including:
                * Step name
                * Element or feature being tested
                * PASS/FAIL/ERROR status
                * Error message (if any)
                * Execution time in seconds (per step)
                

            12. After all tests, print a final report including:

                * Total tests run
                * Number of passes, failures, and errors
                * Total execution time in secound
                * Overall test score as a percentage
                *duration of the step in seconds

            Output only the complete and properly indented Python code. Do not include any explanations or extra commentary.

                        """,
    
        'static': """
            You are an expert QA engineer. Generate a complete and well-structured Selenium test script in Python to test the website: `{url}`.

            Requirements:

            1. Open the browser (Chrome WebDriver) visibly during test execution — do not run in headless mode.
            2. Verify that the base URL loads successfully without errors.
            3. Highlight every interacted element with a 1px solid red border for visual debugging.
            4. Wait for 0.5 seconds after each interaction to simulate natural user behavior.
            5. Perform smooth scrolling up and down the page to ensure all dynamic elements are triggered.
            6. Test a valid login flow using `standard_user` and `secret_sauce` (or appropriate credentials for the site).
            7. Interact with key UI elements:
                * Clickable buttons (e.g., "Add to cart")
                * Dropdowns (e.g., sorting dropdowns)
                * Navigation links (e.g., sidebar, About, Logout)
            8. Highlight and interact with all visible inventory or content items, where applicable.
            9. Simulate tests on three screen sizes:
                * Desktop: 1920x1080
                * Tablet: 768x1024
                * Mobile: 375x667
            10. Ensure that the layout and responsiveness are correct for all screen sizes tested.
            11. After each test, log results including:
                * Step name
                * Element or feature being tested
                * PASS/FAIL/ERROR status
                * Error message (if any)
                * Execution time in seconds (per step)

            12. After all tests, print a final report including:

                * Total tests run
                * Number of passes, failures, and errors
                * Total execution time in secound
                * Overall test score as a percentage
                *duration of the step in seconds

            Output only the complete and properly indented Python code. Do not include any explanations or extra commentary.
        """,
        'dynamic': """
            You are an expert QA engineer. Generate a complete and well-structured Selenium test script in Python to test the website: `{url}`.

            Requirements:

            1. Open the browser (Chrome WebDriver) visibly during test execution — do not run in headless mode.
            2. Verify that the base URL loads successfully without errors.
            3. Highlight every interacted element with a 1px solid red border for visual debugging.
            4. Wait for 0.5 seconds after each interaction to simulate natural user behavior.
            5. Perform smooth scrolling up and down the page to ensure all dynamic elements are triggered.
            6. Test a valid login flow using `standard_user` and `secret_sauce` (or appropriate credentials for the site).
            7. Interact with key UI elements:
                * Clickable buttons (e.g., "Add to cart")
                * Dropdowns (e.g., sorting dropdowns)
                * Navigation links (e.g., sidebar, About, Logout)
            8. Highlight and interact with all visible inventory or content items, where applicable.
            9. Simulate tests on three screen sizes:
                * Desktop: 1920x1080
                * Tablet: 768x1024
                * Mobile: 375x667
            10. Ensure that the layout and responsiveness are correct for all screen sizes tested.
            11. After each test, log results including:
                * Step name
                * Element or feature being tested
                * PASS/FAIL/ERROR status
                * Error message (if any)
                * Execution time in seconds (per step)

            12. After all tests, print a final report including:

                * Total tests run
                * Number of passes, failures, and errors
                * Total execution time in secound
                * Overall test score as a percentage
                *duration of the step in seconds

            Output only the complete and properly indented Python code. Do not include any explanations or extra commentary.

        """,
        'other': """
            You are an expert QA engineer. Generate a complete and well-structured Selenium test script in Python to test the website: `{url}`.

            Requirements:

            1. Open the browser (Chrome WebDriver) visibly during test execution — do not run in headless mode.
            2. Verify that the base URL loads successfully without errors.
            3. Highlight every interacted element with a 1px solid red border for visual debugging.
            4. Wait for 0.5 seconds after each interaction to simulate natural user behavior.
            5. Perform smooth scrolling up and down the page to ensure all dynamic elements are triggered.
            6. Test a valid login flow using `standard_user` and `secret_sauce` (or appropriate credentials for the site).
            7. Interact with key UI elements:
                * Clickable buttons (e.g., "Add to cart")
                * Dropdowns (e.g., sorting dropdowns)
                * Navigation links (e.g., sidebar, About, Logout)
            8. Highlight and interact with all visible inventory or content items, where applicable.
            9. Simulate tests on three screen sizes:
                * Desktop: 1920x1080
                * Tablet: 768x1024
                * Mobile: 375x667
            10. Ensure that the layout and responsiveness are correct for all screen sizes tested.
            11. After each test, log results including:
                * Step name
                * Element or feature being tested
                * PASS/FAIL/ERROR status
                * Error message (if any)
                * Execution time in seconds (per step)
                

            12. After all tests, print a final report including:

                * Total tests run
                * Number of passes, failures, and errors
                * Total execution time in secound
                * Overall test score as a percentage
                *duration of the step in seconds

            Output only the complete and properly indented Python code. Do not include any explanations or extra commentary.

        """
    }
    return templates.get(website_type, templates['other'])

def generate_test_case(url, website_type, custom_prompt=''):
    base_prompt = get_prompt_template(website_type).format(url=url)
    final_prompt = base_prompt + '\n' + custom_prompt if custom_prompt else base_prompt
    
    response = model.generate_content(final_prompt)
    test_code = response.text
    
    # Add imports and setup
    final_code = f"""
{test_code}
"""
    return final_code