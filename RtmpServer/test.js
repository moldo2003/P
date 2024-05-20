const NodeMediaServer = require("node-media-server");

const config = {
  rtmp: {
    port: 1935,
    chunk_size: 60000,
    gop_cache: true,
    ping: 30,
    ping_timeout: 60,
  },
  http: {
    port: 8000,
    allow_origin: "*",
    mediaroot: "./media",
  },
  trans: {
    ffmpeg: "./ffmpeg.exe",
    tasks: [
      {
        app: "live",
        hls: true,
        hlsFlags: "[hls_time=0.5:hls_list_size=1:hls_flags=delete_segments]",
        hlsKeep: false,
      },
    ],
    MediaRoot: "./media",
  },
};

var serverLink = "http://127.0.0.1:5000";

var nms = new NodeMediaServer(config);
nms.on("prePublish", (id, StreamPath, args) => {
  let name = StreamPath.split("/").pop();
  fetch(serverLink + "/newStream/" + name + "/" + id, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
});
nms.on("donePublish", (id, StreamPath, args) => {
  let name = StreamPath.split("/").pop();
  fetch(serverLink + "/streamClosed/" + name + "/" + id, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
});
nms.run();
