class User:
    def __init__(self, name: str, age: int | str, date: str, number: int):
        self.name = name
        self.age = age
        self.date = date
        self.number = number


def get_person_name(one_person: User):
    return one_person.name


def get_user_infos(one_person: User):
    u = one_person
    print(u.name + " Age: " + str(u.age) + " Date of birth: " +
          u.date + " Favorite number: " + str(u.number))
