from playwright.sync_api import sync_playwright

from mfl_adapter.render import displayed_text


def test_displayed_text_handles_html_and_svg_roots():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.set_content(
            """
            <div id="html">
              alpha <span>beta</span>
            </div>

            <svg id="svg"
                 xmlns="http://www.w3.org/2000/svg">
              <text>gamma</text>
              <text>delta</text>
            </svg>
            """
        )

        assert (
            displayed_text(
                page.locator("#html")
            )
            == "alpha beta"
        )

        assert (
            displayed_text(
                page.locator("#svg")
            )
            == "gamma delta"
        )

        browser.close()
