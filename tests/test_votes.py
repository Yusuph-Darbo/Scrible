import pytest

from app import models


def test_vote_on_post(authorized_client, test_posts, session, test_user):
    post_id = test_posts[0].id

    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})

    assert res.status_code == 201
    assert res.json().get("message") == "successful"

    vote = (
        session.query(models.Vote)
        .filter(
            models.Vote.post_id == post_id,
            models.Vote.user_id == test_user["id"],
        )
        .first()
    )
    assert vote is not None


def test_vote_twice_on_post(authorized_client, test_posts):
    post_id = test_posts[0].id

    authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})

    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, session, test_user):
    post_id = test_posts[0].id

    authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 0})

    assert res.status_code == 201
    assert res.json().get("message") == "successfully deleted vote"

    vote = (
        session.query(models.Vote)
        .filter(
            models.Vote.post_id == post_id,
            models.Vote.user_id == test_user["id"],
        )
        .first()
    )
    assert vote is None


def test_delete_vote_non_exist(authorized_client, test_posts):
    post_id = test_posts[0].id

    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 0})

    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client):
    res = authorized_client.post("/vote/", json={"post_id": 88888, "dir": 1})

    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    post_id = test_posts[0].id

    res = client.post("/vote/", json={"post_id": post_id, "dir": 1})

    assert res.status_code == 401


@pytest.mark.parametrize("dir", [-1, 2, 5])
def test_vote_invalid_direction(authorized_client, test_posts, dir):
    post_id = test_posts[0].id

    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": dir})

    assert res.status_code == 422


def test_vote_reflected_in_post_votes_count(authorized_client, test_posts):
    post_id = test_posts[0].id

    authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    res = authorized_client.get(f"/posts/{post_id}")

    assert res.status_code == 200
    assert res.json()["votes"] == 1
