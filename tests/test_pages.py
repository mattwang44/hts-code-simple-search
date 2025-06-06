# /// script
# dependencies = [
#     "pytest-playwright",
#     "pytest",
#     "pytest-asyncio",
# ]
# ///

import pytest
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def server():
    """Return server configuration."""
    return {'port': 8765}


@pytest.fixture
def browser_context_args():
    return {
        'viewport': {
            'width': 1280,
            'height': 720,
        },
    }


async def wait_for_json_content(page, timeout=5000):
    """Wait for JSON content to be loaded and parsed."""
    logger.info('Waiting for JSON content')
    content = await page.locator('#json-content').text_content(timeout=timeout)
    if 'Loading...' in content or 'Error loading JSON' in content:
        await page.wait_for_function(
            "() => !document.getElementById('json-content').textContent.includes('Loading...')", timeout=timeout
        )
        content = await page.locator('#json-content').text_content()
    logger.info('JSON content loaded')
    return json.loads(content)


@pytest.mark.asyncio
async def test_index_page(page, server):
    """Test that the index page loads and displays JSON content."""
    logger.info('Starting index page test')
    await page.goto(f"http://localhost:{server['port']}/index", timeout=5000)
    data = await wait_for_json_content(page)

    assert 'available_codes' in data
    assert 'total_codes' in data
    assert 'example_searches' in data
    assert isinstance(data['available_codes'], list)
    assert len(data['available_codes']) > 0


@pytest.mark.asyncio
async def test_specific_code_page(page, server):
    """Test that a specific HTS code page loads and displays correct data."""
    logger.info('Starting specific code test')
    # Get first code from index
    await page.goto(f"http://localhost:{server['port']}/index", timeout=5000)
    data = await wait_for_json_content(page)
    first_code = data['available_codes'][0]

    # Test the specific code page
    await page.goto(f"http://localhost:{server['port']}/codes/{first_code}", timeout=5000)
    code_data = await wait_for_json_content(page)

    assert 'HTS Number' in code_data
    assert code_data['HTS Number'] == first_code


@pytest.mark.asyncio
async def test_search_functionality(page, server):
    """Test that the search functionality works."""
    logger.info('Starting search functionality test')
    await page.goto(f"http://localhost:{server['port']}/search", timeout=5000)
    search_data = await wait_for_json_content(page)

    # Find a partial code that has matches
    partial_code = None
    for code, data in search_data.items():
        if data['type'] == 'partial' and len(data['matches']) > 0:
            partial_code = code
            break

    assert partial_code is not None

    # Test the partial search
    await page.goto(f"http://localhost:{server['port']}/codes/{partial_code}", timeout=5000)
    partial_data = await wait_for_json_content(page)

    assert partial_data['type'] == 'partial'
    assert len(partial_data['matches']) > 0


@pytest.mark.asyncio
async def test_404_handling(page, server):
    """Test that non-existent codes are handled properly."""
    logger.info('Starting 404 test')
    await page.goto(f"http://localhost:{server['port']}/nonexistent-code", timeout=5000)
    try:
        await wait_for_json_content(page)
        assert False, 'Expected an error for nonexistent code'
    except json.JSONDecodeError:
        content = await page.locator('#json-content').text_content()
        assert 'Error loading JSON' in content
