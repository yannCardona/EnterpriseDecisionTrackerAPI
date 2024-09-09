import os
from django.contrib.auth.models import User, Group
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

try:
    # Create a superuser
    superuser = User.objects.create_superuser(
        username=os.getenv('SUPERUSER_NAME'),
        password=os.getenv('SUPERUSER_PASSWORD')
    )
    # Create or get the 'Admin' group
    admin_group, created = Group.objects.get_or_create(name='Admin')
    # Add the superuser to the 'Admin' group
    superuser.groups.add(admin_group)
    print(f"Superuser '{os.getenv('SUPERUSER_NAME')}' created successfully and added to 'Admin' group.")
except Exception as e:
    print(f"Error creating superuser: {e}")

try:
    # Create a user
    User.objects.create_user(
        username=os.getenv('USER_NAME'),
        password=os.getenv('USER_PASSWORD')
    )
    print(f"User '{os.getenv('USER_NAME')}' created successfully.")
except Exception as e:
    print(f"Error creating user: {e}")
