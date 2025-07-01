from fastapi import APIRouter, status, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.core.config import settings
from app.db.models.books import Books
from app.db.models.reviews import Reviews
from app.dependencies import get_db
from app.utils.response import create_response
from app.db.schema.books import CreateBooks, UpdateBooks
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", summary="Api for entering book data")
async def books(request: CreateBooks, db = Depends(get_db)):
    try:
        query = await db.execute(select(Books).where(Books.book_name == request.book_name, Books.author == request.author))
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
        query = await db.execute(select(Books).where(Books.book_name == request.book_name, Books.author == request.author))
        book = query.scalars().first()
        if not book:
            return create_response(status.HTTP_404_NOT_FOUND, "Book is not found please enter this book data.")
        
        update_data = request.model_dump(exclude_unset=True)
        for key, value in update_data:
            if value not in ("", None):
                setattr(book, key, value)

        await db.commit()

        return create_response(status.HTTP_200_OK, "Book is updated sucesfully")

    except Exception as err:
        logger.error("Error in updating book data api %s", err)
        return create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, settings.INTERNAL_SERVER_ERROR, detail=str(err))
    

@router.get("/", summary="Api for getting book data")
async def get_books(book_id:int = Query(None, description="if want specific book data then enter book_id or want all book data leave this empty"), db = Depends(get_db)):
    try:
        if book_id:
            query = await db.execute(select(Books).options(joinedload(Books.reviews)).where(Books.id == book_id))
            book = query.scalars().first()
            if not book:
                return create_response(status.HTTP_404_NOT_FOUND, "Book is not found given book id")
            
            book_data = {
                "id": book.id,
                "name": book.book_name,
                "author": book.author,
              
                "reviews": [
                    {
                        "id": review.id,
                        "rating": review.rating,
                        "comment": review.comment,
                        "created_at": review.created_at
                    }
                    for review in book.reviews
                ]
            }
            return create_response(status.HTTP_200_OK, "Book and the reviews of book fetched successfully", data={"result": book_data})
        
        query = await db.execute(select(Books))
        books = query.scalars().all()

        return create_response(status.HTTP_200_OK, "All Books data fetched sucesfully", data={"result": books})

    except Exception as err:
        logger.error("Error in getting book data api %s", err)
        return create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, settings.INTERNAL_SERVER_ERROR, detail=str(err))
    


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