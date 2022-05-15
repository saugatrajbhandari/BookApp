def average_rating(rating_list):
    if not rating_list:
        return 0

    return round(sum(rating_list) / len(rating_list))

def check_permission(user):
    return user.has_perm('reviews.add_publisher')