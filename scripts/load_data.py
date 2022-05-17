import datetime
import random

from src.users.models import Organization, User
from src.kudos.models import Kudo


organizations = ['trakstar', 'google', 'amazon', 'facebook', 'netflix']

messages = [
    "Congratulations and BRAVO!",
    "This calls for celebrating! Congratulations!",
    "You did it! So proud of you!",
    "I knew it was only a matter of time. Well done!",
    "Congratulations on your well-deserved success.",
    "Heartfelt congratulations to you.",
    "Warmest congratulations on your achievement.",
    "Congratulations and best wishes for your next adventure!",
    "So pleased to see you accomplishing great things.",
]

first_names = [
    'Omar',
    'Erik',
    'Cassandra',
    'Manuel',
    'Lisa',
    'Cinthya',
    'Charlie',
    'Marie',
    'Kevin',
    'Sofy',
    'Marc',
    'Saly',
    'Jon',
    'Sam',
]

last_names = [
    'Herrera',
    'White',
    'Black',
    'Smith',
    'Williams',
    'Brown',
    'Garcia',
    'Miller',
    'Jones',
    'Ackers',
    'Ackerman',
]


def get_random_date():
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 2, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    last_updated_date = start_date + datetime.timedelta(days=random_number_of_days)
    return last_updated_date


def run():
    # Create Super user
    super_user = User.objects.create_user('admin', password='password')
    super_user.is_superuser = True
    super_user.is_staff = True
    super_user.save()

    # Create Organizations
    org_list = []
    user_list = {

    }
    for org in organizations:
        org_obj = Organization.objects.create(name=org)
        org_list.append(org_obj)
        user_list[org_obj.name] = []

        # Create Users
        for i in range(10):
            last_updated = get_random_date()

            user = User.objects.create(
                last_updated=last_updated,
                kudos_counter=random.randrange(4),
                organization=org_obj,
                first_name=random.choices(first_names)[0],
                last_name=random.choices(last_names)[0],
                username='{}_{}'.format(org_obj.name, i+1)
            )
            user.set_password('password')
            user.save()
            user_list[user.organization.name].append(user)

    for k in range(100):
        random_org = random.choices(org_list)[0]
        from_user, to_user = random.sample(user_list[random_org.name], 2)
        random_message = random.choices(messages)[0]
        message = '{}, {}'.format(to_user.first_name, random_message)

        Kudo.objects.create(
            from_user=from_user,
            to_user=to_user,
            date=get_random_date(),
            message=message,
        )




