
import pytest

from discord.ext.test import message, verify_message, verify_embed, verify_file


pytestmark = pytest.mark.usefixtures("testlos_m")


async def test_colour():
    # TODO: Setup bot permissions
    # await message("^colour #8F008F")
    pytest.skip("Colour testing not yet implemented")
