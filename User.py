class User:
    def __init__(self, name: str):
        self.name = name


def get_person_name(one_person: User):
    return one_person.name

