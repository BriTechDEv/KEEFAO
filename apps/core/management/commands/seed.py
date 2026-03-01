import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import Member
from apps.events.models import Event
from apps.contributions.models import Contribution
from apps.payments.models import Payment
from apps.gallery.models import GalleryImage
from apps.announcements.models import Announcement

class Command(BaseCommand):
    help = "Seeds the database with KEEFAO sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        if not Member.objects.filter(email="admin@keefao.org").exists():
             Member.objects.create_superuser(
             username="admin",  # Added this line
            email="admin@keefao.org",
            password="password123",
            first_name="System",
            last_name="Admin"
             )
        self.stdout.write(self.style.SUCCESS("Created superuser: admin@keefao.org / password123"))

        # 2. Create Sample Members
        members = []
        for i in range(5):
            m, created = Member.objects.get_or_create(
                 email=f"alumni{i}@example.com",
                 defaults={
                 "username": f"alumni{i}", # Adding username here too just in case
                 "first_name": f"Alumnus_{i}",
                 "last_name": "Test",
                 "phone": f"071234567{i}",
                 "kcse_year": 2015 + i,
                 # Make sure this matches your model (contributed vs contributions)
                 "total_contributed": 0 
                 }
            )
            if created:
                m.set_password("password123")
                m.save()
            members.append(m)

        # 3. Create Announcements
        Announcement.objects.get_or_create(
            title="Annual General Meeting 2026",
            defaults={
                "content": "Join us for the upcoming AGM to discuss our impact strategy.",
                "category": "GENERAL",
                "is_active": True
            }
        )

        # 4. Create Events
        event, _ = Event.objects.get_or_create(
            title="KEEF Mentorship Day",
            defaults={
                "description": "Mentoring high school students in Kakamega.",
                "date": timezone.now() + timezone.timedelta(days=15),
                "location": "Kakamega High School",
                "is_active": True
            }
        )

        # 5. Create Payments & Trigger Signals for Contributions
        # We manually create "COMPLETED" payments to test if your signals 
        # generate the Contribution records automatically.
        for i, member in enumerate(members):
            amount = random.choice([500, 1000, 2500, 5000])
            txn_id = f"MPESA_SEED_{random.randint(1000, 9999)}"
            
            # This save() should trigger your apps.payments.signals
            Payment.objects.create(
                user=member,
                contributor_name=f"{member.first_name} {member.last_name}",
                amount=amount,
                method="mpesa",
                status="completed",
                transaction_id=txn_id,
                metadata={"category": "MONTHLY"}
            )
            
        self.stdout.write(self.style.SUCCESS(f"Created {len(members)} members and simulated their payments."))

        # 6. Create Manual/Public Contributions
        Contribution.objects.create(
            contributor_name="Anonymous Wellwisher",
            amount=10000,
            category="WELLWISHER",
            status="VERIFIED",
            message="Keep up the good work!"
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))