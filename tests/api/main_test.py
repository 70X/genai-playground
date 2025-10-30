import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from PIL import Image

from api.main import app


class TestTextToImageEndpoint(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test"""
        self.client = TestClient(app)

    @patch("api.main.save_image")
    @patch("api.main.img_to_bytes")
    @patch("api.main.generate_image")
    def test_generate_image_success(self, mock_generate, mock_img_to_bytes, mock_save):
        """Test successful image generation"""
        # Mock the image generation
        mock_image = MagicMock(spec=Image.Image)
        mock_generate.return_value = mock_image

        # Mock img_to_bytes to return fake image bytes
        fake_image_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        mock_img_to_bytes.return_value = fake_image_bytes

        # Make the request
        response = self.client.get("/generate/image?prompt=a beautiful sunset")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "image/png")
        self.assertEqual(response.content, fake_image_bytes)

        # Verify the functions were called correctly
        mock_generate.assert_called_once()
        mock_save.assert_called_once_with(
            mock_image, "generated_images/a_beautiful_sunset.png"
        )
        mock_img_to_bytes.assert_called_once_with(mock_image)

    @patch("api.main.save_image")
    @patch("api.main.img_to_bytes")
    @patch("api.main.generate_image")
    def test_generate_image_with_spaces_in_prompt(
        self, mock_generate, mock_img_to_bytes, mock_save
    ):
        """Test that spaces in prompt are replaced with underscores in filename"""
        mock_image = MagicMock(spec=Image.Image)
        mock_generate.return_value = mock_image
        mock_img_to_bytes.return_value = b"fake_image_data"

        response = self.client.get("/generate/image?prompt=red car on street")

        self.assertEqual(response.status_code, 200)
        mock_save.assert_called_once_with(
            mock_image, "generated_images/red_car_on_street.png"
        )

    @patch("api.main.save_image")
    @patch("api.main.img_to_bytes")
    @patch("api.main.generate_image")
    def test_generate_image_with_special_characters(
        self, mock_generate, mock_img_to_bytes, mock_save
    ):
        """Test prompt with special characters"""
        mock_image = MagicMock(spec=Image.Image)
        mock_generate.return_value = mock_image
        mock_img_to_bytes.return_value = b"fake_image_data"

        response = self.client.get("/generate/image?prompt=cat & dog!")

        self.assertEqual(response.status_code, 200)
        mock_save.assert_called_once_with(mock_image, "generated_images/cat_&_dog!.png")

    def test_generate_image_missing_prompt(self):
        """Test that missing prompt parameter returns 422"""
        response = self.client.get("/generate/image")

        self.assertEqual(response.status_code, 422)

    @patch("api.main.save_image")
    @patch("api.main.img_to_bytes")
    @patch("api.main.generate_image")
    def test_generate_image_empty_prompt(
        self, mock_generate, mock_img_to_bytes, mock_save
    ):
        """Test with empty prompt string"""
        mock_image = MagicMock(spec=Image.Image)
        mock_generate.return_value = mock_image
        mock_img_to_bytes.return_value = b"fake_image_data"

        response = self.client.get("/generate/image?prompt=")

        self.assertEqual(response.status_code, 200)
        mock_save.assert_called_once_with(mock_image, "generated_images/.png")

    @patch("api.main.save_image")
    @patch("api.main.img_to_bytes")
    @patch("api.main.generate_image")
    def test_generate_image_error_in_generation(
        self, mock_generate, mock_img_to_bytes, mock_save
    ):
        """Test error handling when image generation fails"""
        mock_generate.side_effect = Exception("Model error")

        with self.assertRaises(Exception):
            self.client.get("/generate/image?prompt=test")

    @patch("api.main.save_image")
    @patch("api.main.img_to_bytes")
    @patch("api.main.generate_image")
    def test_generate_image_error_in_save(
        self, mock_generate, mock_img_to_bytes, mock_save
    ):
        """Test error handling when saving image fails"""
        mock_image = MagicMock(spec=Image.Image)
        mock_generate.return_value = mock_image
        mock_img_to_bytes.return_value = b"fake_image_data"
        mock_save.side_effect = IOError("Failed to save")

        with self.assertRaises(IOError):
            self.client.get("/generate/image?prompt=test")


if __name__ == "__main__":
    unittest.main()
