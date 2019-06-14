'use strict';

self.addEventListener('push', function(event) {
  let data = event.data.json();  
  const title = 'PTT八卦報';
  const options = {
    'body': data.msg,
    'data': data.url,
    'icon': '/static/main/img/icon.png',
    'image': '/static/main/img/icon.png',
    'badge': '/static/main/img/icon.png',
    'actions': [
      { 'action': 'confirm', 'title': '確認', 'icon': '/static/main/img/icon.png'},//'/static/main/img/icon.png'
      { 'action': 'cancel', 'title': '取消', 'icon': '/static/main/img/icon.png'}
    ]
  };
  // options中還有其他選項設定：tag、renotify(禁用重複通知的提示default=false)、vibrate(振動頻率)、sound(通知音效)

  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {
  const action = event.action;
  event.notification.close();
  if(action === 'confirm') {
    event.waitUntil(
        clients.openWindow(event.notification.data)
    );
  } 
});

const applicationServerPublicKey = 'BAzkHC_oueOGeuo621Fvxa2Ok95m95QDXqNXtu-0FEmdNtyYjMgHLI8Bp1KemVNE30X4fW40nNNoPthsaI6Z1eE';
///* eslint-enable max-len */

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

// 當訂閱已經or即將失效，會再自動訂閱一次(偷偷來)
self.addEventListener('pushsubscriptionchange', function(event) {
  const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
  event.waitUntil(
    self.registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: applicationServerKey
    })
    .then(function(newSubscription) {
      // TODO: Send to application server
      alert('目前沒有直接的方式可以觸發這個listener，故無從驗證');
      alert('而且fetch預設也不能傳送任何cookie，也就是說session連帶不能使用，所以無法找到對應的login user');
      fetch('/main/subscription/', {
        method: 'get',
        body: JSON.stringify(newSubscription),
        credentials: 'same-origin'  //若fetch的對象與自身網域相同，會提供cookie
      })
      .catch(function(error){
        console.log('fetch failed!', error);
      });
    })
  );
});