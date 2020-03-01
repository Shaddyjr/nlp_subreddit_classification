from gathering_data import format_post_from_json, create_posts_from_json_list

def test_format_post_from_json():
    input_dict = {
        "subreddit"    : "abc",
        "title"        : "def",
        "not_included" : "ghi"
    }
    output = format_post_from_json(input_dict)
    assert type(output) == dict , "should return a dictionary object"

    keys = output.keys()
    assert len(keys) == 2 and "subreddit" in keys and "title" in keys, "should only contain 'subreddit' and 'title' keys"

    assert output.get("subreddit") == input_dict.get("subreddit"), "should faithfully reuse the 'subreddit' information from input"
    assert output.get("title")     == input_dict.get("title"), "should faithfully reuse the 'title' information from input"

def test_create_posts_from_json_list():
    json_list = [
        {"data": {
                "subreddit"    : "abc",
                "title"        : "def"
            }
        },
        {"data": {
                "subreddit"    : "hij",
                "title"        : "klm"
            }
        }
    ]

    output = create_posts_from_json_list(json_list)

    print(output)
    print(json_list[0].get("data").get("subreddit"))
    assert type(output) == list, "should return a list"
    assert all(type(item) == dict for item in output), "should return a list of dictionary objects"
    assert all(item.get("subreddit") == json_list[i].get("data").get("subreddit") for i, item in enumerate(output)), "should return a list of dictionary objects that faithfully reuses the 'subreddit' information from input"
    assert all(item.get("title")     == json_list[i].get("data").get("title")     for i, item in enumerate(output)), "should return a list of dictionary objects that faithfully reuses the 'title' information from input"