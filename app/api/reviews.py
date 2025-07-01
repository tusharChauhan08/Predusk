from fastapi import APIRouter, status, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.core.config import settings
from app.db.models.reviews import Reviews
from app.db.models.books import Books
from app.dependencies import get_db
from app.utils.response import create_response
from app.db.schema.reviews import PostReviews, UpdateReviews
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", summary="Api for posting reviews on book data")
async def post_reviews(request: PostReviews, db = Depends(get_db)):
    try:
        query = await db.execute(select(Reviews).where(Reviews.book_id == request.book_id))
        review = query.scalars().first()
        if review:
            return create_response(status.HTTP_200_OK, "Review is already posted on this book.", data={"result": review})
        
        review_data = Reviews(
            book_id = request.book_id,
            ratings = request.ratings,
            review = request.review,
            reviewer_name = request.reviewer_name
        )
        db.add(review_data)
        await db.commit()

        return create_response(status.HTTP_200_OK, "Review is posted sucesfully")

    except Exception as err:
        logger.error("Error in review posted api %s", err)
        return create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, settings.INTERNAL_SERVER_ERROR, detail=str(err))
    

@router.patch("/", summary="Api for updating reviews")
async def update_review(request: UpdateReviews, db = Depends(get_db)):
    try:
        query = await db.execute(select(Reviews).where(Reviews.id == request.review_id))
        review = query.scalars().first()
        if not review:
            return create_response(status.HTTP_404_NOT_FOUND, "Book review is not found")
        
        update_data = request.model_dump(exclude_unset=True)
        for key, value in update_data:
            if value not in ("", None):
                setattr(review, key, value)

        await db.commit()

        return create_response(status.HTTP_200_OK, "Review is updated sucesfully")

    except Exception as err:
        logger.error("Error in updating review api %s", err)
        return create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, settings.INTERNAL_SERVER_ERROR, detail=str(err))
    

@router.get("/", summary="Api for getting review data")
async def get_reviews(review_id:int = Query(..., description="specific review data then enter review_id"), db = Depends(get_db)):
    try:
        query = await db.execute(select(Reviews).options(joinedload(Reviews.book)).where(Reviews.id == review_id))
        review = query.scalars().first()
        if not review:
            return create_response(status.HTTP_404_NOT_FOUND, "Review is not found given review id")
        
        book = review.book
        
        review_data = {
            "id": review.id,
            "reviewer_name": review.reviewer_name,
            "ratings": review.ratings,
            "reviews": review.reviews,
    
            "book": {
                "id": book.id,
                "book_name": book.book_name,
                "author": book.author,
                "language": book.language,
                "description": book.description,
                "created_at": book.created_at
            } if book else None
        }

        return create_response(status.HTTP_200_OK, "Book data is fetched succesfully", data={"result": review_data})

    except Exception as err:
        logger.error("Error in getting review data api %s", err)
        return create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, settings.INTERNAL_SERVER_ERROR, detail=str(err))
    


@router.delete("/", summary="Api for deleting reviews data")
async def books(review_id:int = Query(..., description="review_id to delete a particular review"), db = Depends(get_db)):
    try:
        query = await db.execute(select(Reviews).where(Reviews.id == book_id))
        book = query.scalars().first()  
        if not book:
            return create_response(status.HTTP_404_NOT_FOUND, "Book is not found please enter this book data.")
        
        await db.delete(book)

        await db.commit()

        return create_response(status.HTTP_200_OK, "Book is deleted sucesfully")

    except Exception as err:
        logger.error("Error in entering book data api %s", err)
        return create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, settings.INTERNAL_SERVER_ERROR, detail=str(err))