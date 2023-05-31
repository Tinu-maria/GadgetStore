from rest_framework.throttling import UserRateThrottle


class ReviewThrottling(UserRateThrottle):
    scope = 'review-throttle'
