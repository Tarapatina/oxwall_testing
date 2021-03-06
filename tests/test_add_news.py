import allure
import pytest
from models.news import News
from data.news_data import news_list


@pytest.fixture(params=news_list, ids=[repr(news) for news in news_list])
def news(request):
    return News(**request.param)


@allure.feature("News (status) CRUD feature")
@allure.story("Create text news creation story")
def test_add_text_news(app, logged_admin, news, db):
    old_amount_of_news = db.count_news()
    app.add_new_news(news)
    app.dash_page.wait_new_news_appearing()
    with allure.step("THEN a newsfeed block is appeared with text '{}' and author as {}".format(
                      news.text, logged_admin.username)):
        assert old_amount_of_news + 1 == db.count_news()
        assert news.text == db.get_last_news().text
        assert news.text == app.dash_page.newsfeeds[0].news_text
        assert logged_admin.username.title() == app.dash_page.newsfeeds[0].user


def test_add_news_with_photo(app, logged_admin):
    pass
