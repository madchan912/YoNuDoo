document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('search-input').value.trim();

    if (query === '') {
        alert('검색어를 입력하세요.');
        return;
    }

    fetch(`/search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById('results');
            resultsContainer.innerHTML = '';

            if (data.length > 0) {
                const list = document.createElement('ul');
                data.forEach(recipe => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `
                        <strong>${recipe.name}</strong><br>
                        재료: ${recipe.ingredients}<br>
                        <a href="${recipe.youtube_url}" target="_blank">유튜브 링크</a>
                    `;
                    list.appendChild(listItem);
                });
                resultsContainer.appendChild(list);
            } else {
                resultsContainer.innerHTML = '<p>검색 결과가 없습니다.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
