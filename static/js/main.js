document.addEventListener("DOMContentLoaded", async function() {
    const searchInput = document.getElementById("ingredient-search");
    const suggestionsList = document.getElementById("suggestions");
    const selectedIngredients = document.getElementById("selected-ingredients");
    const recipeResults = document.getElementById("recipe-results");

    let allRecipes = [];

    async function fetchAllRecipes() {
        try {
            const response = await fetch("/recipes/all");
            if (!response.ok) throw new Error("Failed to fetch recipes");
            allRecipes = await response.json();
            updateRecipes();
        } catch (error) {
            console.error("Error fetching recipes:", error);
        }
    }

    async function fetchFilteredRecipes(selected) {
        try {
            const query = selected.length > 0 ? `?ingredients=${selected.join(",")}` : "";
            const response = await fetch(`/recipes${query}`);
            if (!response.ok) throw new Error("Failed to fetch filtered recipes");
            const recipes = await response.json();
            updateRecipeDisplay(recipes);
        } catch (error) {
            console.error("Error fetching filtered recipes:", error);
        }
    }

    async function fetchAutocomplete(query) {
        try {
            const response = await fetch(`/autocomplete?query=${query}`);
            if (!response.ok) throw new Error("Failed to fetch autocomplete data");
            return await response.json();
        } catch (error) {
            console.error("Error fetching autocomplete data:", error);
            return [];
        }
    }

    searchInput.addEventListener("input", async function() {
        let query = searchInput.value.trim();
        suggestionsList.innerHTML = "";

        if (query.length === 0) return;

        let matches = await fetchAutocomplete(query);
        if (matches.length === 0) return;

        matches.forEach(match => {
            let li = document.createElement("li");
            li.textContent = match;
            li.addEventListener("click", function() {
                addIngredient(match);
                suggestionsList.innerHTML = "";
                searchInput.value = "";
            });
            suggestionsList.appendChild(li);
        });
    });

    function addIngredient(ingredient) {
        if ([...selectedIngredients.children].some(span => span.textContent.includes(ingredient))) return;

        let span = document.createElement("span");
        span.textContent = ingredient;
        span.classList.add("ingredient-item");

        let removeBtn = document.createElement("button");
        removeBtn.textContent = "X";
        removeBtn.classList.add("remove-btn");
        removeBtn.addEventListener("click", function() {
            span.remove();
            updateRecipes();
        });

        span.appendChild(removeBtn);
        selectedIngredients.appendChild(span);

        updateRecipes();
    }

    function updateRecipes() {
        let selected = [...selectedIngredients.children].map(span => span.textContent.replace("X", "").trim());

        if (selected.length === 0) {
            fetchAllRecipes();
        } else {
            fetchFilteredRecipes(selected);
        }
    }

    function updateRecipeDisplay(recipes) {
        recipeResults.innerHTML = recipes.length
            ? recipes.map(recipe =>
                `<p>${recipe.title} - <a href="${recipe.url}" target="_blank">레시피 보기</a></p>`
            ).join("")
            : "<p>해당하는 레시피가 없습니다.</p>";
    }

    fetchAllRecipes();
});
