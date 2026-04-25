from __future__ import annotations
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.permissions import support_required
from reviews.forms import ReviewReplyForm
from reviews.models import Review

@login_required
@support_required
def support_review_list_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `support_review_list_view`.

Args:
    request: Вхідний параметр `request`.

Returns:
    Any: Результат виконання."""
    reviews = Review.objects.select_related('user', 'appointment').order_by('-created_at')
    return render(request, 'avelon_healthcare/reviews/pages/support_review_list.html', {'reviews': reviews})

@login_required
@support_required
def support_review_reply_view(request: HttpRequest, review_id: int) -> HttpResponse:
    """Виконує логіку `support_review_reply_view`.

Args:
    request: Вхідний параметр `request`.
    review_id: Вхідний параметр `review_id`.

Returns:
    Any: Результат виконання."""
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewReplyForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Відповідь збережено.')
            return redirect('reviews:support_review_list')
    else:
        form = ReviewReplyForm(instance=review)
    return render(request, 'avelon_healthcare/reviews/pages/support_review_reply.html', {'form': form, 'review': review})
