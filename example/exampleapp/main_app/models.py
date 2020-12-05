from django.db import models


class Venue(models.Model):
    """Model definition for Venue."""

    title = models.CharField(max_length=88)
    capacity = models.PositiveIntegerField()

    class Meta:
        """Meta definition for Venue."""

        verbose_name = 'Venue'
        verbose_name_plural = 'Venues'

    def __str__(self):
        """Unicode representation of Venue."""
        return self.title


class Play(models.Model):
    """Model definition for Play."""

    title = models.CharField(max_length=255)

    class Meta:
        """Meta definition for Play."""

        verbose_name = 'Play'
        verbose_name_plural = 'Plays'

    def __str__(self):
        """Unicode representation of Play."""
        return self.title


class Performance(models.Model):
    """Model definition for Performance."""

    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    staged_at = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    sold_out = models.BooleanField()

    class Meta:
        """Meta definition for Performance."""

        verbose_name = 'Performance'
        verbose_name_plural = 'Performances'

    def __str__(self):
        """Unicode representation of Performance."""
        return f"Play {self.play_id} performed at {self.date}"


class TicketQuerySet(models.QuerySet):

    def with_comment(self):
        return self.all().set_label("annotated query")


class Ticket(models.Model):
    """Model definition for Ticket."""

    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    
    objects = TicketQuerySet.as_manager()

    class Meta:
        """Meta definition for Ticket."""

        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        """Unicode representation of Ticket."""
        return f"Ticket {self.id}; cost: {self.price}"
