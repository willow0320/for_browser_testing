document.addEventListener('DOMContentLoaded', function() {
    // 저장된 설정 불러오기
    chrome.storage.sync.get(['urls'], function(result) {
        if (result.urls) {
            result.urls.forEach(url => {
                addUrlToList(url);
            });
        }
    });

    // URL 추가 버튼 클릭 시
    document.getElementById('add-url-btn').addEventListener('click', function() {
        var urlInput = document.getElementById('url-input');
        var newUrl = urlInput.value.trim();
        
        if (newUrl !== '') {
            addUrlToList(newUrl);
            urlInput.value = '';

            // 저장된 URL 리스트 업데이트
            chrome.storage.sync.get(['urls'], function(result) {
                var urls = result.urls || [];
                urls.push(newUrl);
                chrome.storage.sync.set({ 'urls': urls });
            });
        }
    });

    // URL 삭제 버튼 클릭 시
    document.getElementById('url-list').addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-btn')) {
            var urlToRemove = e.target.parentNode.dataset.url;

            // URL 리스트에서 삭제
            chrome.storage.sync.get(['urls'], function(result) {
                var urls = result.urls || [];
                var updatedUrls = urls.filter(url => url !== urlToRemove);
                chrome.storage.sync.set({ 'urls': updatedUrls });

                // 화면에서 삭제
                e.target.parentNode.remove();
            });
        }
    });

    // URL 리스트에 URL 추가하기
    function addUrlToList(url) {
        var urlList = document.getElementById('url-list');
        var li = document.createElement('li');
        li.dataset.url = url;
        li.textContent = url;
        
        var deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.classList.add('delete-btn');
        li.appendChild(deleteBtn);

        urlList.appendChild(li);
    }
});
