class TestData:
    VALID_USER = ("student1", "Pass123!")

    INVALID_USERS = [
        ("wrong_user", "fail3347!"),
        ("student1", "incorrect_faile"),
        ("", "fail3347!"),
        ("student1", ""),
    ]
