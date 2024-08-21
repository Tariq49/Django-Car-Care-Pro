from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

class CustomerFeedback(models.Model):
    
    service_id = models.ForeignKey('ServiceRequest', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comments = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['service_id'],
                name='unique_feedback_per_service'
            ),
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name='rating_between_1_and_5'
            ),
        ]

    def __str__(self):
        
        customer_name = self.service_id.customer.user.get_full_name() if self.service_id.customer.user else "Unknown Customer"
        service_name = self.service_id.service_name
        problem_description = self.service_id.problem_description
        rating = self.rating
        comments = self.comments or "No comments provided"

        return (f"{customer_name} | "
                f"{service_name} | "
                f"{problem_description} | "
                f"Rating: {rating} | "
                f"Comments: {comments}")