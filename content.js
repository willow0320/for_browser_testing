// 예시: 메시지를 수신하고 처리하는 스크립트
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === 'RestartRecording') {
    // Start recording logic
    console.log('Recording started...');
  } else if (message.action === 'stopRecording') {
    // Stop recording logic
    console.log('Recording stopped.');
  }
});
