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

            if (query === "") {
                resultsContainer.innerHTML = "";  // 검색어가 없을 때 결과 비우기
                return;
            }

            // 서버에 검색 쿼리 전송
            fetch(`/search?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.results.length === 0) {
                        noResultsPopup.classList.add('active');
                    } else {
                        noResultsPopup.classList.remove('active');
                        // 결과를 DOM에 업데이트
                        resultsContainer.innerHTML = data.results.map(recipe => {
                            // 검색어 볼드 처리
                            var highlightedIngredients = recipe.ingredients.replace(new RegExp(query, 'gi'), (match) => `<strong>${match}</strong>`);

                            return `
                                <div class="grid-item">
                                    <h2>${recipe.name}</h2>
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

    // 팝업 닫기 버튼 클릭 시 동작 (저장 팝업)
    if (closePopupButton) {
        closePopupButton.addEventListener('click', function () {
            savePopup.classList.remove('active');  // 팝업 숨김
        });
    }
});
