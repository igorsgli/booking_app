from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.bookings.router import add_booking, get_bookings, remove_booking
from app.hotels.router import get_hotel_by_id, get_hotels_by_location_ant_time
from app.hotels.rooms.router import get_rooms_by_time
from app.utils import format_number_thousand_separator, get_month_days


router = APIRouter(
    prefix='/pages',
    tags=['Фронтенд']
)

templates = Jinja2Templates(directory='app/templates')

@router.get('/login', response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse(
        'auth/login.html',
        {'request': request},
    )

@router.get('/register', response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse(
        'auth/register.html',
        {'request': request}
    )

@router.get('/hotels/{location}', response_class=HTMLResponse)
async def get_hotels_page(
    request: Request,
    location: str,
    date_from: date,
    date_to: date,
    hotels=Depends(get_hotels_by_location_ant_time)
):
    dates = get_month_days()
    if date_from > date_to:
        date_to, date_from = date_from, date_to
    # Автоматически ставим дату заезда позже текущей даты
    date_from = max(datetime.today().date(), date_from)

    return templates.TemplateResponse(
        'hotels_and_rooms/hotels.html',
        {
            'request': request,
            'hotels': hotels,
            'location': location,
            'date_to': date_to.strftime('%Y-%m-%d'),
            'date_from': date_from.strftime('%Y-%m-%d'),
            'dates': dates,
        },
    )

@router.get('/hotels/{hotel_id}/rooms', response_class=HTMLResponse)
async def get_rooms_page(
    request: Request,
    date_from: date,
    date_to: date,
    rooms=Depends(get_rooms_by_time),
    hotel=Depends(get_hotel_by_id),
):
    date_from_formatted = date_from.strftime('%d.%m.%Y')
    date_to_formatted = date_to.strftime('%d.%m.%Y')
    booking_length = (date_to - date_from).days
    return templates.TemplateResponse(
        'hotels_and_rooms/rooms.html',
        {
            'request': request,
            'hotel': hotel,
            'rooms': rooms,
            'date_from': date_from,
            'date_to': date_to,
            'booking_length': booking_length,
            'date_from_formatted': date_from_formatted,
            'date_to_formatted': date_to_formatted,
        },
    )

@router.get('/successful_booking', response_class=HTMLResponse)
async def get_successful_booking_page(
    request: Request,
    _=Depends(add_booking),
):
    return templates.TemplateResponse(
        'bookings/booking_successful.html',
        {'request': request},
    )


@router.get('/deleted_booking', response_class=HTMLResponse)
async def get_deleted_booking_page(
    request: Request,
    _=Depends(remove_booking),
):
    return templates.TemplateResponse(
        'bookings/booking_deleted.html',
        {'request': request},
    )

@router.get('/bookings', response_class=HTMLResponse)
async def get_bookings_page(
    request: Request,
    bookings=Depends(get_bookings),
):
    return templates.TemplateResponse(
        'bookings/bookings.html',
        {
            'request': request,
            'bookings': bookings,
            'format_number_thousand_separator': format_number_thousand_separator,
        },
    )
