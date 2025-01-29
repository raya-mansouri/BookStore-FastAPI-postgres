from app.celery_worker import celery_app
from sqlalchemy.orm import Session
from app.models.book import Book
from app.services.reservation_service import ReservationService
from app.dependency import get_db

@celery_app.task
def process_reservation_queue():
    db: Session = get_db()
    books = db.query(Book).all()  
    for book in books:
        service = ReservationService(db, None, book.id, 0)
        service.process_queue()
    db.close()
