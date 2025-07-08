# # src/metrics.py

# from sqlalchemy import select, func, and_
# from datetime import date, datetime
# from db.models import Activity, Subscriber


# async def calculate_daily_metrics(session, channel_id: int) -> dict:
#     """
#     Расчёт ежедневных метрик по каналу:
#     - общее количество подписчиков
#     - количество подписок за сегодня
#     - количество отписок за сегодня
#     """
#     today = date.today()

#     # Общее кол-во подписчиков
#     stmt_total = select(func.count()).select_from(Subscriber).where(
#         Subscriber.channel_id == channel_id
#     )
#     total = (await session.execute(stmt_total)).scalar()

#     # Подписки за сегодня
#     stmt_joins = select(func.count()).select_from(Activity).where(
#         and_(
#             Activity.channel_id == channel_id,
#             Activity.type == "join",
#             func.date(Activity.timestamp) == today
#         )
#     )
#     joins = (await session.execute(stmt_joins)).scalar()

#     # Отписки за сегодня
#     stmt_lefts = select(func.count()).select_from(Activity).where(
#         and_(
#             Activity.channel_id == channel_id,
#             Activity.type == "left",
#             func.date(Activity.timestamp) == today
#         )
#     )
#     lefts = (await session.execute(stmt_lefts)).scalar()

#     return {
#         "subs_total": total,
#         "subs_today": joins,
#         "unsubs_today": lefts,
#         "timestamp": datetime.now()
#     }
