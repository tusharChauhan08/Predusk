from fastapi import APIRouter, status, Depends, Query
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from app.core.config import settings
from app.db.models.books import Books
from app.db.models.reviews import Reviews
from app.dependencies import get_db
from app.utils.response import create_response
from app.db.schema.books import CreateBooks, UpdateBooks
from app.utils.cache import get_cached_data, set_cached_data
import redis.asyncio as redis
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", summary="Api for entering book data")
async def books(request: CreateBooks, db = Depends(get_db)):
    try:
        query = await db.execute(select(Books).where(and_(
            Books.book_name == request.book_name,
            Books.author == request.author
        )))
        print(query)
        book = query.scalars().first()
        if book:
            return create_response(status.HTTP_200_OK, "Book is already present in db", data={"result": book})
        
        book_data = Books(
            book_name = request.book_name,
            author = request.author,
            description = request.description,
            language = request.language
        )
        db.add(book_data)
        await db.commit()

        return create_response(status.HTTP_200_OK, "Book is entered sucesfully")

    except Exception as err:
        logger.error("Error in entering book data api %s", err)
        return create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, settings.INTERNAL_SERVER_ERROR, detail=str(err))
    

@router.patch("/", summary="Api for updating book data")
async def update_books(request: UpdateBooks, db = Depends(get_db)):
    try:
        query = await db.execute(select(Books).where(Books.id == request.id))
        book = query.scalars().first()
        if not book:
            return create_response(status.HTTP_404_NOT_FOUND, "Book is not found please enter this book data.")
        
        update_data = request.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value not in ("", None):
                setattr(book, key, value)

        await db.commit()

        return create_response(status.HTTP_200_OK, "Book is updated sucesfully")

    except Exception as err:
        logger.error("Error in updating book data api %s", err)
        return create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, settings.INTERNAL_SERVER_ERROR, detail=str(err))
    

@router.get("/", summary="API for getting book data")
async def get_books(book_id: int = Query(None, description="If you want specific book data then enter book_id, or leave empty for all books"), db=Depends(get_db)):
    try:
        if book_id:
            cache_key = f"book:{book_id}"
            cached_book = await get_cached_data(cache_key)
            if cached_book:
                return create_response(status.HTTP_200_OK, "Book fetched from cache", data={"result": cached_book})

            query = await db.execute(
                select(Books)
                .options(joinedload(Books.reviews))
                .where(Books.id == book_id)
            )
            book = query.scalars().first()

            if not book:
                return create_response(status.HTTP_404_NOT_FOUND, "Book not found for the given ID")

            book_data = {
                "id": book.id,
                "name": book.book_name,
                "author": book.author,
                "language": book.language,
                "description": book.description,
                "created_at": book.created_at.isoformat() if isinstance(book.created_at, datetime) else None,
                "updated_at": book.updated_at.isoformat() if isinstance(book.updated_at, datetime) else None,
                "reviews": [
                    {
                        "id": review.id,
                        "ratings": review.ratings,
                        "review": review.review,
                        "created_at": review.created_at.isoformat() if isinstance(review.updated_at, datetime) else None,
                        "updated_at": review.updated_at.isoformat() if isinstance(review.updated_at, datetime) else None,
                    }
                    for review in book.reviews
                ]
            }

            await set_cached_data(cache_key, book_data)
            return create_response(status.HTTP_200_OK, "Book fetched from database", data={"result": book_data})


        cache_key = "books:all"
        cached_books = await get_cached_data(cache_key)
        if cached_books:
            return create_response(status.HTTP_200_OK, "Books fetched from cache", data={"result": cached_books})

        query = await db.execute(select(Books))
        books = query.scalars().all()

        books_data = [
            {
                "id": book.id,
                "name": book.book_name,
                "author": book.author,
                "description": book.description,
                "language": book.language
            } for book in books
        ]

        await set_cached_data(cache_key, books_data)
        return create_response(status.HTTP_200_OK, "Books fetched from database", data={"result": books_data})

    except Exception as err:
        logger.error("Error in /books API: %s", err)
        return create_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            settings.INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    


@router.delete("/", summary="Api for deleting book data")
async def books(book_id:int = Query(..., description="book_id to delete a particular book"), db = Depends(get_db)):
    try:
        query = await db.execute(select(Books).where(Books.id == book_id))
        book = query.scalars().first()  
        if not book:
            return create_response(status.HTTP_404_NOT_FOUND, "Book is not found please enter this book data.")
        
        await db.delete(book)

        await db.commit()

        return create_response(status.HTTP_200_OK, "Book is deleted sucesfully")

    except Exception as err:
        logger.error("Error in deleting book data api %s", err)
        return create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, settings.INTERNAL_SERVER_ERROR, detail=str(err))