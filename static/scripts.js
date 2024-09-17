document.addEventListener('DOMContentLoaded', function () {
    var searchButton = document.getElementById('search-button');
    var noResultsPopup = document.getElementById('no-results-popup');
    var closePopupButton = document.getElementById('close-popup');
    var searchInput = document.getElementById('search-input');
    var resultsContainer = document.getElementById('results');
    var saveForm = document.getElementById('save-form');
    var savePopup = document.getElementById('save-popup');
    var popupMessage = document.getElementById('popup-message');

    // 검색 버튼 클릭 시 동작
    if (searchButton) {
        searchButton.addEventListener('click', function () {
            var query = searchInput.value.trim();

            // 검색어가 없더라도 서버에 검색 요청을 보냅니다.
            fetch(`/search?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.results.length === 0) {
                        noResultsPopup.classList.add('active');
                    } else {
                        noResultsPopup.classList.remove('active');

                        // 검색어 강조 (이름과 재료에서)
                        const queryRegex = new RegExp(query, 'gi'); // 대소문자 구분 없이 검색어 찾기
                        resultsContainer.innerHTML = data.results.map(recipe => {
                            const highlightedName = recipe.name.replace(queryRegex, match => `<strong>${match}</strong>`);
                            const highlightedIngredients = recipe.ingredients.replace(queryRegex, match => `<strong>${match}</strong>`);

                            return `
                                <div class="grid-item">
                                    <h2>${highlightedName}</h2>
                                    <p>${highlightedIngredients}</p>
                                    <a href="${recipe.youtube_url}" target="_blank">유튜브 링크</a>
                                </div>
                            `;
                        }).join('');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }

    // 팝업 닫기 버튼 클릭 시 동작 (검색 결과 없음 팝업)
    if (closePopupButton) {
        closePopupButton.addEventListener('click', function () {
            noResultsPopup.classList.remove('active');  // 팝업 숨김
        });
    }

    // 저장 버튼 클릭 시 동작
    if (saveForm) {
        saveForm.addEventListener('submit', function (event) {
            event.preventDefault();  // 기본 폼 제출 동작 방지
            var formData = new FormData(saveForm);

            fetch('/save', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())  // JSON 응답으로 파싱
            .then(data => {
                popupMessage.textContent = data.message;  // 서버에서 받은 메시지 표시
                savePopup.classList.add('active');  // 팝업 표시
                if (data.success) {
                    saveForm.reset();  // 성공 시 폼 리셋
                }
            })
            .catch(error => {
                console.error('Error:', error);
                popupMessage.textContent = '저장 중 오류가 발생했습니다. 다시 시도해 주세요.';
                savePopup.classList.add('active');
            });
        });
    }
});
