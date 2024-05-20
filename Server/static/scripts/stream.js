window.onload = async function () {
  var socket = io();
  let streamKey = window.location.pathname.split("/").pop();

  function init() {
    // Get the stream key from the URL

    // Create the HLS stream URL
    const hlsUrl = `http://192.168.100.16:8000/live/${streamKey}/index.m3u8`;

    // Create the video element
    const video = document.getElementById("stream");

    // Check if browser natively supports HLS
    if (video.canPlayType("application/vnd.apple.mpegurl")) {
      // If the browser supports HLS natively, set the source of the video element to the HLS stream URL
      video.src = hlsUrl;
    } else if (Hls.isSupported()) {
      // If the browser does not support HLS natively but hls.js is supported, use hls.js to play the HLS stream
      const hls = new Hls({
        // Number of times to retry loading when an error occurs
        manifestLoadingMaxRetry: 3,
        levelLoadingMaxRetry: 3,
        fragLoadingMaxRetry: 3,
      });
      hls.loadSource(hlsUrl);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, function () {
        //video.play();
      });
    } else {
      console.error("This is a legacy browser that doesnt support MSE");
    }
  }

  function renderMessage(message) {
    const messagesContainer = document.getElementById("messages");

    console.log(message);

    const messageContainer = document.createElement("div");
    messageContainer.className = "messageContainer";

    const messageElement = document.createElement("div");
    messageElement.className = "message";
    messageElement.innerText = message["message"];

    const userContainer = document.getElementById("users");
    const userElement = document.createElement("div");
    userElement.className = "user";
    userElement.style.color = message["color"];
    userElement.innerText = message["user_name"] + " : ";

    messageContainer.appendChild(userElement);
    messageContainer.appendChild(messageElement);

    messagesContainer.appendChild(messageContainer);
  }

  function playVideo() {
    const video = document.getElementById("stream");
    video.play();
  }

  function pauseVideo() {
    const video = document.getElementById("stream");
    video.pause();
  }

  socket.on("connect", () => {
    let user = JSON.parse(localStorage.getItem("user"));
    socket.emit("joinStream", streamKey, user["username"]);
  });

  socket.on("disconnect", () => {
    // This code will run when the client disconnects
    // You can also emit a message to the server
    window.location.href = "/";
  });

  socket.on("streamCloased", (users) => {
    alert("Stream was closed");
    window.location.href = "/";
  });
  socket.on("newMessage", (message) => {
    console.log(message);
    renderMessage(message);
  });
  socket.on("syncMessages", (messages) => {
    console.log(messages);
    messages.forEach((message) => {
      renderMessage(message);
    });
  });

  document.getElementById("back").addEventListener("click", async function () {
    let user = JSON.parse(localStorage.getItem("user"));
    await socket.emit("leftStream", streamKey, user["username"]);
    window.location.href = "/";
  });
  document.getElementById("sendButton").addEventListener("click", () => {
    const message = document.getElementById("messageInput").value.trim();
    if (message !== "") {
      // Emit the message to the server
      socket.emit(
        "sentMessage",
        streamKey,
        message,
        JSON.parse(localStorage.getItem("user"))["username"]
      );
      // Clear the input field after sending the message
      messageInput.value = "";
    }
  });

  init();
};
