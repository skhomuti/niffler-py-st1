from unittest.mock import Mock

import pytest

from clients.spends_client import SpendsHttpClient
from conftest import spends_generator
from models.spend import Category, Spend, SpendAdd


@pytest.fixture
def client():
    c = SpendsHttpClient("", "")
    c.session = Mock()
    return c


class SpendsClientMock:
    spends: list[Spend] = []

    def add_spends(self, spend: SpendAdd) -> Spend:
        spend = Spend(
            id="1",
            amount=spend.amount,
            description=spend.description,
            category=spend.category,
            spendDate=spend.spendDate,
            currency=spend.currency
        )
        self.spends.append(spend)
        return spend

    def get_spends(self) -> list[Spend]:
        return self.spends

    def remove_spends(self, ids: list[str]):
        self.spends = [spend for spend in self.spends if spend.id not in ids]


def test_category(client):
    client.session.get = Mock(return_value=Mock(json=Mock(return_value=[
        {"id": "1", "category": "test", "username": "test"}
    ])))
    categories = client.get_categories()
    assert len(categories) == 1
    assert categories == [Category(id="1", category="test", username="test")]


def test_spends_generator():
    spend_client = SpendsClientMock()
    spends_gen = spends_generator(spends_client=spend_client, spend=SpendAdd(amount=10, description="test", category="test", spendDate="2021-01-01", currency="USD"))
    spend = next(spends_gen)
    assert spend in spend_client.spends

    next(spends_gen, None)

    assert spend not in spend_client.spends
