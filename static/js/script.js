document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.querySelector('#recipes-table tbody');
    const titleFilter = document.getElementById('title-filter');
    const cuisineFilter = document.getElementById('cuisine-filter');
    const drawer = document.getElementById('recipe-drawer');
    const drawerContent = document.getElementById('drawer-content');
    const closeDrawerBtn = document.getElementById('close-drawer');
    const drawerOverlay = document.getElementById('drawer-overlay');

    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');
    const limitSelect = document.getElementById('limit-select');

    const noDataMsg = document.getElementById('no-data-message');
    const noResultsMsg = document.getElementById('no-results-message');
    const paginationControls = document.querySelector('.pagination');
    const recipesTable = document.getElementById('recipes-table');

    let currentPage = 1;
    let totalPages = 1;
    let currentLimit = parseInt(limitSelect.value, 10);
    let searchMode = false;

    async function fetchData(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching data:', error);
            return null;
        }
    }

    function renderTable(recipes) {
        tableBody.innerHTML = '';
        if (!recipes || recipes.length === 0) return;

        recipes.forEach(recipe => {
            const row = document.createElement('tr');
            row.addEventListener('click', () => openDrawer(recipe));

            const rating = recipe.rating ? Math.round(recipe.rating) : 0;
            const stars = '&#9733;'.repeat(rating) + '&#9734;'.repeat(5 - rating);

            row.innerHTML = `
                <td class="title-cell">${recipe.title || 'N/A'}</td>
                <td>${recipe.cuisine || 'N/A'}</td>
                <td><span class="star-rating">${stars}</span></td>
                <td>${recipe.total_time || 'N/A'}</td>
                <td>${recipe.serves || 'N/A'}</td>
            `;
            tableBody.appendChild(row);
        });
    }

    function updateUI(data, isSearch) {
        const recipes = isSearch ? data.data : data.data;
        const totalItems = isSearch ? recipes.length : data.total;

        renderTable(recipes);

        recipesTable.style.display = totalItems > 0 ? 'table' : 'none';
        paginationControls.style.display = totalItems > 0 && !isSearch ? 'flex' : 'none';

        noDataMsg.style.display = totalItems === 0 && !isSearch ? 'block' : 'none';
        noResultsMsg.style.display = totalItems === 0 && isSearch ? 'block' : 'none';

        if (!isSearch) {
            currentPage = data.page;
            totalPages = Math.ceil(data.total / data.limit);
            pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
            prevPageBtn.disabled = currentPage === 1;
            nextPageBtn.disabled = currentPage >= totalPages;
        }
    }

    async function loadRecipes(page = 1, limit = currentLimit) {
        searchMode = false;
        const data = await fetchData(`/api/recipes?page=${page}&limit=${limit}`);
        if (data) {
            updateUI(data, false);
        }
    }

    async function handleSearch() {
        const title = titleFilter.value.trim();
        const cuisine = cuisineFilter.value.trim();

        if (title === '' && cuisine === '') {
            if (searchMode) {
                loadRecipes(1, currentLimit);
            }
            return;
        }

        searchMode = true;
        let searchUrl = '/api/recipes/search?';
        const params = [];
        if (title) params.push(`title=${encodeURIComponent(title)}`);
        if (cuisine) params.push(`cuisine=${encodeURIComponent(cuisine)}`);

        const data = await fetchData(searchUrl + params.join('&'));
        if (data) {
            updateUI(data, true);
        }
    }

    function openDrawer(recipe) {
        drawerContent.innerHTML = `
            <h2>${recipe.title}</h2>
            <p><strong>Cuisine:</strong> ${recipe.cuisine}</p>
            <div class="detail-item">
                <strong>Description:</strong>
                <p>${recipe.description}</p>
            </div>
            <div class="detail-item expand-section">
                <strong class="expand-toggle">Total Time: ${recipe.total_time} min &#9662;</strong>
                <div class="expand-content">
                    <p>Prep Time: ${recipe.prep_time} min</p>
                    <p>Cook Time: ${recipe.cook_time} min</p>
                </div>
            </div>
            <div class="detail-item">
                <strong>Nutrition:</strong>
                <table class="nutrition-table">
                    ${Object.entries(recipe.nutrients).map(([key, value]) => `<tr><td>${key.replace(/([A-Z])/g, ' $1').trim()}</td><td>${value}</td></tr>`).join('')}
                </table>
            </div>
        `;
        drawer.classList.add('open');
        drawerOverlay.classList.add('visible');

        drawerContent.querySelector('.expand-toggle').addEventListener('click', (e) => {
            e.currentTarget.parentElement.classList.toggle('open');
        });
    }

    function closeDrawer() {
        drawer.classList.remove('open');
        drawerOverlay.classList.remove('visible');
    }

    titleFilter.addEventListener('input', handleSearch);
    cuisineFilter.addEventListener('input', handleSearch);

    prevPageBtn.addEventListener('click', () => { if (currentPage > 1) loadRecipes(currentPage - 1, currentLimit); });
    nextPageBtn.addEventListener('click', () => { if (currentPage < totalPages) loadRecipes(currentPage + 1, currentLimit); });
    limitSelect.addEventListener('change', (e) => {
        currentLimit = parseInt(e.target.value, 10);
        loadRecipes(1, currentLimit);
    });

    closeDrawerBtn.addEventListener('click', closeDrawer);
    drawerOverlay.addEventListener('click', closeDrawer);

    loadRecipes(currentPage, currentLimit);
});
