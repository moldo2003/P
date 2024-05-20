let user = undefined;
let streams = [];

function logout() {
  localStorage.removeItem("auth");
  window.location.href = "/login";
}

function copyToClipboard() {
  navigator.clipboard
    .writeText(user.streamKey)
    .then(function () {
      alert("Stream key copied to clipboard");
    })
    .catch(function () {
      alert("Failed to copy stream key to clipboard");
    });
}

window.onload = async function () {
  var socket = io();

  function onInit() {
    let auth = localStorage.getItem("auth");
    if (auth == null) {
      window.location.href = "/login";
    } else {
      fetch("/verifyToken", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          token: auth,
        }),
      }).then((res) => {
        if (res.status == 200) {
        } else {
          localStorage.removeItem("auth");
          window.location.href = "/login";
        }
      });

      fetch("/getUser/" + auth, {
        method: "GET",
        headers: {
          "Content-Type": "application",
        },
      }).then((res) => {
        res.json().then((data) => {
          user = data;
          if (data.profilePic != "")
            document.querySelector(".avatar").src = `/img/${data.profilePic}`;
            localStorage.setItem("user", JSON.stringify(user));
          socket.emit("join", user.streamKey);
        });
      });
    }
  }

  async function fetchStreams() {
    try {
      const response = await fetch("/getStreams"); // Replace '/api/streams' with your actual API endpoint
      if (!response.ok) {
        throw new Error("Failed to fetch streams");
      }
      const streams = await response.json();
      return streams;
    } catch (error) {
      console.error("Error fetching streams:", error);
      return [];
    }
  }

  async function renderStreams() {
    const streamsContainer = document.getElementById("streams-container");
    streamsContainer.innerHTML = ""; // Clear existing content

    try {
      const Streams = await fetchStreams();

      if (Streams.length == 0) {
        const streamContainer = document.createElement("p");
        streamContainer.textContent = "No streams available";
        streamContainer.classList.add("no-streams");
        streamsContainer.appendChild(streamContainer);
        return;
      }

      Streams.forEach((stream) => {
        // Create a container for each stream
        const streamContainer = document.createElement("div");
        streamContainer.classList.add("card");
        streamContainer.addEventListener("click", function () {
          window.location.href = `/watch/${stream.stream_key}`;
        });

        // Create an image element for the thumbnail
        const thumbnailImg = document.createElement("img");
        thumbnailImg.src = `/getThumbnail/${stream.stream_key}`; // Set src to the URL of the thumbnail
        thumbnailImg.alt = "Thumbnail";
        thumbnailImg.classList.add("thumbnail");
        streamContainer.appendChild(thumbnailImg);

        const description = document.createElement("div");
        description.classList.add("description");
        streamContainer.appendChild(description);
        // Create profile picture
        const profilePic = document.createElement("img");
        profilePic.src = `/img/${stream.profilePic}`;
        profilePic.alt = "Profile Picture";
        profilePic.classList.add("profilePic");
        description.appendChild(profilePic);
        // Create a paragraph element for the stream name
        const streamNamePara = document.createElement("p");
        streamNamePara.textContent = stream.streamer_name;
        description.appendChild(streamNamePara);
        // Append the stream container to the streamsContainer
        streamsContainer.appendChild(streamContainer);
      });
    } catch (error) {
      console.error("Error rendering streams:", error);
    }
  }

  document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0];
    const username = user.username; // Replace with the actual username

    const formData = new FormData();
    formData.append("file", file);
    formData.append("username", username);

    fetch("/uploadImage", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        location.reload(true);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

  document.querySelector(".avatar").addEventListener("click", function () {
    document.querySelector(".hamburger").classList.toggle("open");
  });

  document.body.addEventListener("click", function (event) {
    // Check if the click is outside of the hamburger menu
    if (
      !event.target.closest(".hamburger") &&
      !event.target.closest(".avatar")
    ) {
      // If the hamburger menu is open, close it
      if (document.querySelector(".hamburger").classList.contains("open")) {
        document.querySelector(".hamburger").classList.remove("open");
      }
    }
  });

  socket.on("message", function (event) {
    console.log("Message from server: ", event);
  });

  socket.on("newStream", async function (streamKey) {
    const streams = await fetchStreams();
    renderStreams(streams);
  });

  socket.on("streamCloased", async function (streamKey) {
    const streams = await fetchStreams();
    renderStreams(streams);
  });


  
  onInit();
  const streams = await fetchStreams();
  renderStreams(streams);
};
