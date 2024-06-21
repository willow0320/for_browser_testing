chrome.runtime.onInstalled.addListener(function() {
    // 액션 버튼 클릭 시 options.html을 dialog 형태로 띄우기
    chrome.action.onClicked.addListener(function(tab) {
        chrome.windows.create({
            url: 'options.html',
            type: 'popup',
            width: 600,
            height: 400
        });
    });
});
