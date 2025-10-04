// Get the search form and input field
const searchForm = document.querySelector('.search-form');
const searchInput = document.querySelector('.search-form input[type="text"]');

// Add an event listener to the search form
searchForm.addEventListener('submit', (e) => {
    // Prevent the default form submission behavior
    e.preventDefault();

    // Get the search query
    const query = searchInput.value.trim();

    // Check if the search query is not empty
    if (query !== '') {
        // Submit the form
        searchForm.submit();
    }
});
