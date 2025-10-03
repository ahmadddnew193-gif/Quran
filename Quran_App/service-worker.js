self.addEventListener("push", function(event) {
  const data = event.data.json();
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: "https://upload.wikimedia.org/wikipedia/commons/6/6b/Quran_Kareem.png"
    })
  );
});
