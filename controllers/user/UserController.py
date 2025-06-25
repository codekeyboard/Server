from fastapi import HTTPException
from models.AppUser import AppUser

class UserController:

    @staticmethod
    async def list(request):
        users = await AppUser.select()
        return users

    @staticmethod
    async def get(request):
        user_id = request.path_params.get("id")
        user = await AppUser.objects().get_or_none(AppUser.id == int(user_id))
        if not user:
            raise HTTPException(404, "User not found")
        return user

    @staticmethod
    async def create(request):
        data = await request.json()
        user = await AppUser(**data).save().returning()
        return user

    @staticmethod
    async def update(request):
        user_id = request.path_params.get("id")
        user = await AppUser.objects().get_or_none(AppUser.id == int(user_id))
        if not user:
            raise HTTPException(404, "User not found")
        data = await request.json()
        for k, v in data.items():
            setattr(user, k, v)
        await user.save()
        return user

    @staticmethod
    async def delete(request):
        user_id = request.path_params.get("id")
        user = await AppUser.objects().get_or_none(AppUser.id == int(user_id))
        if not user:
            raise HTTPException(404, "User not found")
        await user.remove()
        return {"message": "User deleted"}
