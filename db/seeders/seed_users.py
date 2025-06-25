import os, sys

sys.path.append(os.path.abspath(os.path.join(__file__, "../../../")))

from tables import AppUser

async def run():
    await AppUser.insert().add(
        AppUser(name="Ali", email="ali@example.com"),
        AppUser(name="Sara", email="sara@example.com"),
    )