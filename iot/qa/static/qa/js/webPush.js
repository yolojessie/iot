const applicationServerPublicKey = 'BKg6rcFJvhWkKDFlhANEaSu6lZ5BeNlq2RUDVSSVaHK5vvAEi9zgB8sJAiDN4uU7yhB9Sy2qAeE7s_RyHlc4rZo';//'BAzkHC_oueOGeuo621Fvxa2Ok95m95QDXqNXtu-0FEmdNtyYjMgHLI8Bp1KemVNE30X4fW40nNNoPthsaI6Z1eE';
const pushButton = document.querySelector('.js-push-btn');

let isSubscribed = false;
let swRegistration = null;

function urlB64ToUint8Array(base64String) {
  // 公鑰是base64編碼，這裡要轉為VAPID接受的Uint8Array
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


//function updateBtn() {
//  if (Notification.permission === 'denied') {
//    pushButton.textContent = 'Push Messaging Blocked.';
//    pushButton.disabled = true;
//    updateSubscriptionOnServer(null);
//    return;
//  }
//  
//  if (isSubscribed) {
//    pushButton.textContent = '關閉通知';
//  } else {
//    pushButton.textContent = '接受通知';
//  }
//
//  pushButton.disabled = false;
//}

function updateSubscriptionOnServer(subscription) {
  // Send subscription to application server
//  const subscriptionJson = document.querySelector('.js-subscription-json');
//  const subscriptionDetails = document.querySelector('.js-subscription-details');
  $.ajax({
    url: '/qa/subscription/',
    type: 'GET',
    data: {
      'data':JSON.stringify(subscription),
    }
  })
//  .done(function(){
//    if (subscription) {
//      subscriptionJson.textContent = JSON.stringify(subscription);
//      subscriptionDetails.classList.remove('is-invisible');
//    } else {
//      subscriptionDetails.classList.add('is-invisible');
//    }
//  });
  
}


function subscribeUser() {
  const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
  swRegistration.pushManager.subscribe({
    userVisibleOnly: true,    //使用者收到通知時能否顯示
    applicationServerKey: applicationServerKey
  })
  .then(function(subscription) {
    
    updateSubscriptionOnServer(subscription);
    console.log('User is subscribed:', subscription);
    isSubscribed = true;
//    updateBtn();
    
//    alert('發訂閱消息到後端');
  })
  .catch(function(err) {
    console.log('Failed to subscribe the user: ', err);
//    updateBtn();
  });
}

function unsubscribeUser() {
  swRegistration.pushManager.getSubscription()
  .then(function(subscription) {
    if (subscription) {
      // TODO: Tell application server to delete subscription
      alert('刪除訂閱');
      return subscription.unsubscribe();
    }
  })
  .catch(function(error) {
    console.log('Error unsubscribing', error);
  })
  .then(function() {
    updateSubscriptionOnServer(null);

//    console.log('User is unsubscribed.');
    isSubscribed = false;

//    updateBtn();
  });
}

function initialiseUI() {
//    if (!isSubscribed) subscribeUser();
//    } else {
//      unsubscribeUser();
//    }

  // Set the initial subscription value
  swRegistration.pushManager.getSubscription()
  .then(function(subscription) {
    isSubscribed = !(subscription === null);

//    updateSubscriptionOnServer(subscription);
    if (isSubscribed) {
      console.log('User IS subscribed.',subscription);
    } else {
      console.log('User is NOT subscribed.');
      subscribeUser();
    }
//    updateBtn();
  });
  

}


if ('serviceWorker' in navigator && 'PushManager' in window) {
  console.log('Service Worker and Push is supported');
  window.addEventListener('load', function() {//載入後再註冊
    navigator.serviceWorker.register('/serviceworker.js')
    .then(function(swReg) {
    console.log('Service Worker is registered', swReg);

    swRegistration = swReg;
    initialiseUI();
    })
    .catch(function(error) {
    console.error('Service Worker Error', error);
    });
  });
} else {
  console.warn('Push messaging is not supported');
  //pushButton.textContent = 'Push Not Supported';
}