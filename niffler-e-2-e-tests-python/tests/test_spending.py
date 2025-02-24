import pytest
from selene import browser, have, command
from marks import Pages, TestData
from models.spend import SpendAdd, CategoryAdd

pytestmark = [pytest.mark.allure_label("Spendings", label_type="epic")]


@Pages.main_page
def test_spending_title_exists():
    browser.element('#spendings').should(have.text('History of Spendings'))

TEST_CATEGORY = "school"


@pytest.fixture()
def main_page_late(category, spends, envs):
    browser.open(envs.frontend_url)


@pytest.mark.usefixtures("main_page_late")
@TestData.category(TEST_CATEGORY)
@TestData.spends(
    SpendAdd(
        amount=108.51,
        description="QA.GURU Python Advanced 1",
        category=CategoryAdd(name=TEST_CATEGORY),
        spendDate="2024-08-08T18:39:27.955Z",
        currency="RUB"
    )
)
def test_spending_should_be_deleted_after_table_action(category, spends):
    browser.element('#spendings tbody').should(have.text("QA.GURU Python Advanced 1"))
    browser.element('#spendings tbody .MuiCheckbox-root').perform(command.js.scroll_into_view).click()
    browser.element('#delete').click()
    browser.element("//div[@role='dialog']//button[contains(text(),'Delete')]").click()

    browser.all("#spendings tbody tr").should(have.size(0))
    browser.element('#spendings').should(have.text("There are no spendings"))
