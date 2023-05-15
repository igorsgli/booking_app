import asyncio
from datetime import date
from typing import List, Optional

from fastapi import APIRouter
from pydantic import parse_obj_as

from app.exceptions import CannotBookHotelForLongPeriod, DateFromCannotBeAfterDateTo
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelInfo
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix='/hotels',
    tags=['Отели'],
)

@router.get('/{location}')
@cache(expire=30)
async def get_hotels_by_location_ant_time(
    location: str,
    date_from: date,
    date_to: date
) -> List[SHotelInfo]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels

@router.get('/id/{hotel_id}')
async def get_hotel_by_id(
    hotel_id: int
) -> Optional[SHotel]: 
    return await HotelDAO.find_one_or_none(id=hotel_id)
