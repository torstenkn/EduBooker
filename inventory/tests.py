from django.test import TestCase
from django.conf import settings
from users.models import CustomUser  # Import your custom user model
from .models import MediaCategory, LibrarySite, MediaType
from inventory.functions import validate_isbn13
from django.utils import timezone

class MediaCategoryModelTest(TestCase):

    def setUp(self):
        # Create a test user using the custom user model
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='12345')

    def test_create_media_category(self):
        """Test creating a valid media category."""
        category = MediaCategory.objects.create(
            code='LTB',
            name='Sachbücher Naturwissenschaften Tiere Pflanzen',
            colour='green',
            colour_code='#00ff00',
            description='Books about science and nature.',
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(category.code, 'LTB')
        self.assertEqual(category.name, 'Sachbücher Naturwissenschaften Tiere Pflanzen')
        self.assertEqual(category.colour, 'green')
        self.assertEqual(category.colour_code, '#00ff00')
        self.assertEqual(category.description, 'Books about science and nature.')
        self.assertEqual(category.created_by, self.user)
        self.assertEqual(category.updated_by, self.user)

    def test_unique_code_constraint(self):
        """Test that the code field must be unique."""
        MediaCategory.objects.create(
            code='LTB',
            name='Category 1',
            colour='blue',
            colour_code='#0000ff',
            created_by=self.user,
            updated_by=self.user
        )

        with self.assertRaises(Exception):
            MediaCategory.objects.create(
                code='LTB',
                name='Category 2',
                colour='red',
                colour_code='#ff0000',
                created_by=self.user,
                updated_by=self.user
            )

    def test_invalid_colour_code(self):
        """Test that an invalid hex colour code raises a validation error."""
        with self.assertRaises(Exception):
            MediaCategory.objects.create(
                code='SCI',
                name='Science Books',
                colour='red',
                colour_code='invalid_color_code',  # Invalid hex format
                created_by=self.user,
                updated_by=self.user
            )

    def test_optional_description_field(self):
        """Test that the description field can be left blank."""
        category = MediaCategory.objects.create(
            code='ART',
            name='Art Books',
            colour='purple',
            colour_code='#800080',
            description='',  # Blank description
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(category.description, '')

    def test_str_representation(self):
        """Test the string representation of the model."""
        category = MediaCategory.objects.create(
            code='BIO',
            name='Biology Books',
            colour='green',
            colour_code='#00ff00',
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(str(category), 'BIO - Biology Books')

    def test_timestamps(self):
        """Test that timestamps are automatically set on creation and update."""
        category = MediaCategory.objects.create(
            code='HIS',
            name='History Books',
            colour='brown',
            colour_code='#8B4513',
            created_by=self.user,
            updated_by=self.user
        )
        self.assertIsNotNone(category.created_at)
        self.assertIsNotNone(category.updated_at)
        
class LibrarySiteModelTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='12345')

    def test_create_library_site(self):
        """Test creating a valid library site."""
        site = LibrarySite.objects.create(
            name="Central Library",
            description="The main library in the city center.",
            opening_hours="Mon-Fri: 9am-6pm",
            is_active=True,
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(site.name, "Central Library")
        self.assertEqual(site.description, "The main library in the city center.")
        self.assertEqual(site.opening_hours, "Mon-Fri: 9am-6pm")
        self.assertTrue(site.is_active)
        self.assertEqual(site.created_by, self.user)
        self.assertEqual(site.updated_by, self.user)

    def test_unique_name_constraint(self):
        """Test that the library site name must be unique."""
        LibrarySite.objects.create(
            name="Central Library",
            description="First library site",
            created_by=self.user,
            updated_by=self.user
        )
        
        with self.assertRaises(Exception):
            # Attempt to create another site with the same name should raise an error
            LibrarySite.objects.create(
                name="Central Library",
                description="Second library site",
                created_by=self.user,
                updated_by=self.user
            )

    def test_inactive_site(self):
        """Test creating a library site and marking it as inactive."""
        site = LibrarySite.objects.create(
            name="North Branch Library",
            description="A branch library in the north part of the city.",
            is_active=False,
            created_by=self.user,
            updated_by=self.user
        )
        self.assertFalse(site.is_active)

    def test_optional_fields(self):
        """Test that optional fields like description and opening_hours can be blank."""
        site = LibrarySite.objects.create(
            name="West Branch Library",
            description="",
            opening_hours="",
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(site.description, "")
        self.assertEqual(site.opening_hours, "")

    def test_timestamps(self):
        """Test that timestamps are automatically set on creation and update."""
        site = LibrarySite.objects.create(
            name="East Branch Library",
            description="A branch library in the east.",
            created_by=self.user,
            updated_by=self.user
        )
        self.assertIsNotNone(site.created_at)
        self.assertIsNotNone(site.updated_at)
        self.assertAlmostEqual(site.created_at, timezone.now(), delta=timezone.timedelta(seconds=1))
        self.assertAlmostEqual(site.updated_at, timezone.now(), delta=timezone.timedelta(seconds=1))

    def test_str_representation(self):
        """Test the string representation of the LibrarySite model."""
        site = LibrarySite.objects.create(
            name="South Branch Library",
            description="A branch library in the south part of the city.",
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(str(site), "South Branch Library")
        
class MediaTypeModelTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='12345')

    def test_create_media_type(self):
        """Test creating a valid media type."""
        media_type = MediaType.objects.create(
            name="Book",
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(media_type.name, "Book")
        self.assertEqual(media_type.created_by, self.user)
        self.assertEqual(media_type.updated_by, self.user)

    def test_unique_name_constraint(self):
        """Test that the media type name must be unique."""
        MediaType.objects.create(
            name="Book",
            created_by=self.user,
            updated_by=self.user
        )
        
        with self.assertRaises(Exception):
            # Attempt to create another media type with the same name should raise an error
            MediaType.objects.create(
                name="Book",
                created_by=self.user,
                updated_by=self.user
            )

    def test_timestamps(self):
        """Test that timestamps are automatically set on creation and update."""
        media_type = MediaType.objects.create(
            name="Music CD",
            created_by=self.user,
            updated_by=self.user
        )
        self.assertIsNotNone(media_type.created_at)
        self.assertIsNotNone(media_type.updated_at)

    def test_str_representation(self):
        """Test the string representation of the MediaType model."""
        media_type = MediaType.objects.create(
            name="Game",
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(str(media_type), "Game")
        
class ISBN13ValidationTest(TestCase):

    def test_valid_isbn13_string(self):
        """Test that a valid ISBN-13 as a string is correctly validated."""
        isbn = "9781861972712"
        self.assertTrue(validate_isbn13(isbn))

    def test_valid_isbn13_number(self):
        """Test that a valid ISBN-13 as a number is correctly validated."""
        isbn = 9781861972712
        self.assertTrue(validate_isbn13(isbn))

    def test_invalid_isbn13_wrong_check_digit(self):
        """Test that an ISBN-13 with an incorrect check digit fails validation."""
        isbn = "9781861972718"  # Incorrect check digit
        self.assertFalse(validate_isbn13(isbn))

    def test_invalid_isbn13_too_short(self):
        """Test that an ISBN-13 with fewer than 13 digits fails validation."""
        isbn = "97818619727"  # Only 11 digits
        self.assertFalse(validate_isbn13(isbn))

    def test_invalid_isbn13_too_long(self):
        """Test that an ISBN-13 with more than 13 digits fails validation."""
        isbn = "978186197271234"  # 15 digits
        self.assertFalse(validate_isbn13(isbn))

    def test_invalid_isbn13_non_numeric(self):
        """Test that a non-numeric ISBN-13 fails validation."""
        isbn = "97818619727AB"  # Contains letters
        self.assertFalse(validate_isbn13(isbn))

    def test_invalid_input_type(self):
        """Test that an invalid input type (e.g. list) fails validation."""
        isbn = [9781861972712]  # Invalid type (list instead of number or string)
        self.assertFalse(validate_isbn13(isbn))
        
        
from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import CustomUser
from .models import Media, MediaCategory, MediaType, LibrarySite

class MediaModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='12345')
        self.category = MediaCategory.objects.create(code='T', name='Tiergeschichten', created_by=self.user)
        self.media_type = MediaType.objects.create(name='Book', created_by=self.user)
        self.site = LibrarySite.objects.create(name='Central Library', created_by=self.user)

    def test_media_number_with_legacy(self):
        """Test that the media_number is set using the legacy_media_number if provided."""
        media = Media.objects.create(
            title="Legacy Media",
            site=self.site,
            category=self.category,
            media_type=self.media_type,
            legacy_media_number="0015",
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(media.media_number, "T0015")

    def test_media_number_without_legacy(self):
        """Test that the media_number is set automatically when no legacy_media_number is provided."""
        Media.objects.create(
            title="First Media",
            site=self.site,
            category=self.category,
            media_type=self.media_type,
            media_number="T0001",
            created_by=self.user,
            updated_by=self.user
        )
        
        media = Media.objects.create(
            title="Auto-generated Media",
            site=self.site,
            category=self.category,
            media_type=self.media_type,
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(media.media_number, "T0002")

    def test_media_number_starting_at_0001(self):
        """Test that media_number starts at 0001 if there are no media items in the category."""
        media = Media.objects.create(
            title="First in Category",
            site=self.site,
            category=self.category,
            media_type=self.media_type,
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(media.media_number, "T0001")