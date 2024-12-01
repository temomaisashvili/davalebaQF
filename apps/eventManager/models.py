from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from datetime import timedelta

class Customer(models.Model):
    username = models.CharField(max_length=100, verbose_name="იუზერნეიმი")
    first_name = models.CharField(max_length=100, verbose_name="სახელი", default="")
    email = models.EmailField("ელ.ფოსტის მისამართი", unique=True)
    is_active = models.BooleanField("აქტიურია", default=False)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} ".strip() or self.email

    @staticmethod
    def username_contains_string_and_is_active(contained_string):
        """
        TODO: Write a query using Q objects to filter customers
        whose usernames contain a specific string (case-insensitive)
        AND who are active.
        """
        return Customer.objects.filter(
            Q(username__icontains=contained_string) & Q(is_active=True)
        )

    @staticmethod
    def customers_with_email_or_username(email_or_username):
        """
        TODO: Write a query using Q objects to return customers whose email
        OR username matches a given string (case-insensitive).
        """
        return Customer.objects.filter(
            Q(email__iexact=email_or_username) | Q(username__iexact=email_or_username)
        )

    @staticmethod
    def inactive_customers_registered_after(date):
        """
        TODO: Write a query using Q objects to return all inactive customers
        who registered after a specific date.
        """
        return Customer.objects.filter(
            Q(is_active=False) & Q(date_joined__gt=date)
        )

    @staticmethod
    def customers_with_similar_emails(email_part):
        """
        TODO: Write a query using Q objects to return customers whose email
        contains a specific part (case-insensitive), but only if the email ends with '.com'.
        """
        return Customer.objects.filter(
            Q(email__icontains=email_part) & Q(email__endswith=".com")
        )

    get_full_name.verbose_name = "სრული სახელი"

    class Meta:
        ordering = ("-id",)
        verbose_name = "მომხმარებელი"
        verbose_name_plural = "მომხმარებლები"

class Stadium(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    capacity = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    @staticmethod
    def stadiums_with_name_and_capacity(name, min_capacity):
        """
        TODO: Write a query using Q objects to return stadiums whose name contains
        a specific string (case-insensitive) AND whose capacity is greater than a specified amount.
        """
        return Stadium.objects.filter(
            Q(name__icontains=name) & Q(capacity__gt=min_capacity)
        )

    @staticmethod
    def stadiums_with_capacity_in_range(min_capacity, max_capacity):
        """
        TODO: Write a query using Q objects to return stadiums whose capacity is
        BETWEEN a specified minimum and maximum value.
        """
        return Stadium.objects.filter(
            Q(capacity__gte=min_capacity) & Q(capacity__lte=max_capacity)
        )

    @staticmethod
    def stadiums_not_in_city(city):
        """
        TODO: Write a query using Q objects to return stadiums that are NOT
        located in a specific city.
        """
        return Stadium.objects.exclude(
            address__icontains=city
        )

    @staticmethod
    def stadiums_in_city_or_high_capacity(city, min_capacity):
        """
        TODO: Write a query using Q objects to return stadiums located in a
        specific city OR with a capacity greater than a specified amount.
        """
        return Stadium.objects.filter(
            Q(address__icontains=city) | Q(capacity__gt=min_capacity)
        )

class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateTimeField(null=False, blank=False)
    stadium = models.ForeignKey(Stadium, null=False, blank=False, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField("აქტიურია", null=False, default=True)

    def __str__(self):
        return self.name

    @staticmethod
    def events_in_year_or_active(year):
        """
        TODO: Write a query using Q objects to return events that either
        occur in a specified year OR are active.
        """
        return Event.objects.filter(
            Q(date__year=year) | Q(is_active=True)
        )

    @staticmethod
    def events_in_stadium_with_min_capacity(stadium_name, min_capacity):
        """
        TODO: Write a query using Q objects to return events taking place at
        a specified stadium where the stadium capacity is greater than a specified amount.
        """
        return Event.objects.filter(
            Q(stadium__name__icontains=stadium_name) & Q(stadium__capacity__gt=min_capacity)
        )

    @staticmethod
    def events_not_active_or_past():
        """
        TODO: Write a query using Q objects to return events that are either
        NOT active OR have a date in the past.
        """
        return Event.objects.filter(
            Q(is_active=False) | Q(date__lt=now())
        )

    @staticmethod
    def events_with_keyword_and_date_range(keyword, start_date, end_date):
        """
        TODO: Write a query using Q objects to return events whose name contains
        a specific keyword (case-insensitive) AND occur between two specified dates.
        """
        return Event.objects.filter(
            Q(name__icontains=keyword) & Q(date__range=(start_date, end_date))
        )

class Ticket(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    bought_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.customer} -- {self.event}"

    @staticmethod
    def tickets_by_customer_or_event(customer_id, event_id):
        """
        TODO: Write a query using Q objects to return tickets bought by a
        specific customer OR for a specific event.
        """
        return Ticket.objects.filter(
            Q(customer__id=customer_id) | Q(event__id=event_id)
        )

    @staticmethod
    def recent_tickets_excluding_event(event_id, days=30):
        """
        TODO: Write a query using Q objects to return tickets purchased
        in the last specified number of days, but exclude those for a specified event.
        """
        pass

    @staticmethod
    def tickets_by_customer_with_event_in_year(customer_id, year):
        """
        TODO: Write a query using Q objects to return tickets bought by a specific
        customer for events occurring in a specified year.
        """
        return Ticket.objects.filter(
            Q(customer__id=customer_id) & Q(event__date__year=year)
        )

    @staticmethod
    def tickets_for_events_with_keyword(keyword):
        """
        TODO: Write a query using Q objects to return tickets for events
        whose names contain a specific keyword (case-insensitive).
        """
        return Ticket.objects.filter(
            Q(event__name__icontains=keyword)
        )