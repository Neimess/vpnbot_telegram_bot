from datetime import datetime, timedelta
from database.connection import get_session, database
from database.models import User
from sqlalchemy import update, select

async def create_user(telegram_id: int, name: str, token: str = None) -> User:
    """
    Создаёт нового пользователя в базе данных.
    """
    async with database() as db:
            result = await db.execute(select(User).filter(User.telegram_id == telegram_id))
            existing_user = result.scalars().first()

            if existing_user:
                return existing_user

            user = User(
                telegram_id=telegram_id,
                name=name,
                access_token=token
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

async def get_user(telegram_id: int) -> User:
    """
    Возвращает пользователя по Telegram ID.
    """
    async with database() as db:
        result = await db.execute(select(User).filter(User.telegram_id == telegram_id))
        user = result.scalars().first()
        return user

async def update_user_token(telegram_id: int, new_token: str) -> User:
    """
    Обновляет токен пользователя.
    """
    async with database() as db:
            result = await db.execute(select(User).filter(User.telegram_id == telegram_id))
            user = result.scalars().first()
            if user:
                user.access_token = new_token
                user.updated_at = datetime.now()
                await db.commit()
                await db.refresh(user)
            return user

async def delete_user(telegram_id: int) -> bool:
    """
    Удаляет пользователя по Telegram ID.
    """
    async with database() as db:
            result = await db.execute(select(User).filter(User.telegram_id == telegram_id))
            user = result.scalars().first()
            if user:
                await db.delete(user)
                await db.commit()
                return True
            return False

async def get_user_label(telegram_id: int) -> str:
    async with database() as db:
        result = await db.execute(select(User).filter(User.telegram_id == telegram_id))
        user = result.scalars().first()
        if user:
            return user.label
    return ""

async def update_user_label(telegram_id: int, label: str) -> bool:
    async with database() as db:
        result = await db.execute(select(User).filter(User.telegram_id == telegram_id))
        user = result.scalars().first()
        if user:
            user.label = label
            user.label_at = datetime.now()
            user.updated_at = datetime.now()
            await db.commit()
            return True
    return False

async def confirm_local_payment(telegram_id: int):
    async with database() as db:
        await db.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(
                is_paid=True,
                expires_at=datetime.now() + timedelta(days=30),
                updated_at=datetime.now()
            )
        )
        await db.commit()