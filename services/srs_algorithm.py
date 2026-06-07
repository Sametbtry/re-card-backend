from datetime import datetime, timedelta

def calculate_sm2(grade: int, iterations: int, interval: int, ease_factor: float, next_review_date: datetime = None) -> tuple[int, int, float, str, datetime]:
    """
    SM-2 (Spaced Repetition) Algorithm
    grade: 1 (Unuttum), 2 (Zor), 3 (Kolay)
    """
    if grade >= 2:
        if iterations == 0:
            interval = 1
        elif iterations == 1:
            interval = 6
        else:
            interval = round(interval * ease_factor)
        iterations += 1
    else:
        iterations = 0
        interval = 1

    # Map our 1-3 grade to the traditional 0-5 SM2 grade for ease factor formula
    # Our grades: 1=Hatırlamadım, 2=Zor, 3=Kolay
    # SM2 grades: 1=Again(1), 3=Hard(3), 5=Easy(5)
    if grade <= 1:
        sm2_grade = 1
    elif grade == 2:
        sm2_grade = 3
    else:
        sm2_grade = 5

    ease_factor = ease_factor + (0.1 - (5 - sm2_grade) * (0.08 + (5 - sm2_grade) * 0.02))

    # Gecikme cezası uygulaması (kart gecikmişse ve başarıyla hatırlanmışsa)
    if next_review_date and grade >= 2:
        # Zaman dilimi bilgisini temizle
        if next_review_date.tzinfo is not None:
            scheduled_date = next_review_date.astimezone().replace(tzinfo=None).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            scheduled_date = next_review_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        days_overdue = (today - scheduled_date).days
        if days_overdue > 0:
            # Gecikilen gün başına 0.02 azalt, maksimum 0.2 azalt
            penalty = min(0.02 * days_overdue, 0.2)
            ease_factor -= penalty

    if ease_factor < 1.3:
        ease_factor = 1.3

    status = "mastered" if interval >= 21 else "learning"
    # ignore clock information (00:00:00)
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    next_review_date_val = today + timedelta(days=interval)

    return iterations, interval, ease_factor, status, next_review_date_val
