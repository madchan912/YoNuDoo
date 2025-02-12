document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("ingredient-search");
    const suggestionsList = document.getElementById("suggestions");
    const selectedIngredients = document.getElementById("selected-ingredients");

    // ✅ 백엔드 API에서 자동완성 데이터 가져오기
    async function fetchAutocomplete(query) {
        try {
            const response = await fetch(`/autocomplete?query=${query}`);
            if (!response.ok) {
                throw new Error("Failed to fetch autocomplete data");
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching autocomplete data:", error);
            return [];
        }
    }

    // ✅ 검색창 입력 이벤트 처리
    searchInput.addEventListener("input", async function() {
        let query = searchInput.value.trim();
        suggestionsList.innerHTML = ""; // ✅ 기존 목록 초기화

        if (query.length === 0) {
            return;
        }

        let matches = await fetchAutocomplete(query); // ✅ 백엔드 API에서 자동완성 데이터 가져오기

        if (matches.length === 0) {
            return;
        }

        matches.forEach(match => {
            let li = document.createElement("li");
            li.textContent = match;
            li.addEventListener("click", function() {
                addIngredient(match);
                suggestionsList.innerHTML = ""; // ✅ 클릭하면 자동완성 목록 숨김
                searchInput.value = ""; // ✅ 선택 후 입력창 초기화
            });
            suggestionsList.appendChild(li);
        });
    });

    // ✅ 선택된 재료 추가 함수
    function addIngredient(ingredient) {
        let existingItems = selectedIngredients.getElementsByClassName("ingredient-item");
        for (let item of existingItems) {
            if (item.textContent.includes(ingredient)) {
                return; // ✅ 중복 추가 방지
            }
        }

        let span = document.createElement("span");
        span.textContent = ingredient;
        span.classList.add("ingredient-item");

        let removeBtn = document.createElement("button");
        removeBtn.textContent = "X";
        removeBtn.classList.add("remove-btn");
        removeBtn.addEventListener("click", function() {
            span.remove();
        });

        span.appendChild(removeBtn);
        selectedIngredients.appendChild(span);
    }
});