import pytest

from app import schemas, models


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_list = list(map(validate, res.json()))

    assert res.status_code == 200
    assert len(posts_list) == len(test_posts)


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_get_all_posts_empty(authorized_client):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200
    assert res.json() == []


def test_get_posts_search(authorized_client, test_posts):
    res = authorized_client.get("/posts/", params={"search": "first"})
    posts = res.json()

    assert res.status_code == 200
    assert len(posts) == 1
    assert posts[0]["post"]["title"] == "first title"


def test_get_posts_limit(authorized_client, test_posts):
    res = authorized_client.get("/posts/", params={"limit": 2})
    posts = res.json()

    assert res.status_code == 200
    assert len(posts) == 2


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert res.status_code == 200
    assert post.post.id == test_posts[0].id
    assert post.post.title == test_posts[0].title
    assert post.post.content == test_posts[0].content
    assert post.votes == 0


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/88888")
    assert res.status_code == 404


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("favorite pizza", "i love pepperoni", False),
        ("tallest skyscrapers", "wahoo", True),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "arbitrary content"}
    )

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.published == True
    assert created_post.user_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "arbitrary content"}
    )
    assert res.status_code == 401


def test_create_post_missing_fields(authorized_client):
    res = authorized_client.post("/posts/", json={"content": "missing a title"})
    assert res.status_code == 422


def test_delete_post_success(authorized_client, test_user, test_posts, session):
    post_id = test_posts[0].id

    res = authorized_client.delete(f"/posts/{post_id}")
    assert res.status_code == 204

    deleted_post = session.query(models.Post).filter(models.Post.id == post_id).first()
    assert deleted_post is None


def test_delete_post_non_exist(authorized_client, test_posts):
    res = authorized_client.delete("/posts/88888")
    assert res.status_code == 404


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_other_user_post(authorized_client, test_posts):
    # test_posts[3] belongs to test_user2, authorized_client is authenticated as test_user
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post_success(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True,
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True,
    }
    # test_posts[3] belongs to test_user2, authorized_client is authenticated as test_user
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}", json={})
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True,
    }
    res = authorized_client.put("/posts/88888", json=data)
    assert res.status_code == 404
