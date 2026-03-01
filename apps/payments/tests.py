from django.test import TestCase
from apps.accounts.models import Member
from apps.payments.models import Payment
from apps.contributions.models import Contribution
from decimal import Decimal

class PaymentSignalTest(TestCase):
    def setUp(self):
        """Create a test member to receive the contribution."""
        self.member = Member.objects.create_user(
            email="testmember@keefao.org",
            password="testpassword123",
            first_name="Test",
            last_name="Member",
            kcse_year=2020
        )
        # Ensure initial balance is zero
        self.member.total_contributions = Decimal("0.00")
        self.member.save()

    def test_payment_success_creates_contribution_and_updates_balance(self):
        """
        Scenario: A payment is marked as 'COMPLETED'.
        Expected: 1. A Contribution object is created.
                  2. Member's balance increases by the payment amount.
        """
        payment_amount = Decimal("500.00")
        payment_ref = "TEST_REF_123"

        # Create a payment (This should trigger your signal when saved)
        payment = Payment.objects.create(
            member=self.member,
            amount=payment_amount,
            status="PENDING",
            payment_method="MPESA",
            transaction_id=payment_ref
        )

        # Simulate the 'COMPLETED' status update (as a webhook would)
        payment.status = "COMPLETED"
        payment.save()

        # 1. Verify Contribution creation
        contribution_exists = Contribution.objects.filter(
            payment_reference=payment_ref,
            member=self.member
        ).exists()
        self.assertTrue(contribution_exists, "Contribution record was not created by the signal.")

        # 2. Verify Member balance update
        # We need to refresh from DB to get the signal's changes
        self.member.refresh_from_db()
        self.assertEqual(
            self.member.total_contributions, 
            payment_amount, 
            f"Member balance expected {payment_amount}, but found {self.member.total_contributions}"
        )

    def test_duplicate_payment_prevention(self):
        """
        Scenario: The same payment is saved twice as 'COMPLETED'.
        Expected: Only one Contribution should exist (Idempotency).
        """
        payment = Payment.objects.create(
            member=self.member,
            amount=Decimal("100.00"),
            status="COMPLETED",
            transaction_id="UNIQUE_TXN_99"
        )
        
        # Save again without changes
        payment.save()

        contribution_count = Contribution.objects.filter(payment_reference="UNIQUE_TXN_99").count()
        self.assertEqual(contribution_count, 1, "Duplicate contributions were created for the same payment.")