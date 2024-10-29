let currentVideoIndex = 0;
let videos = [];

function loadVideo(index) {
    const videoPlayer = document.getElementById('video-player');
    const source = document.getElementById('video-source');
    const subtitleTrack = document.getElementById('subtitle-track');

    source.src = videos[index].url;
    subtitleTrack.src = videos[index].subtitle;
    videoPlayer.load();
}

function fetchVideos() {
    fetch('/api/videos')
        .then(response => response.json())
        .then(data => {
            videos = data;
            loadVideo(0);
        });
}

function goLive() {
    // Example function to handle live video logic
    // This could be more complex based on metadata fetched from your S3 or backend logic
    loadVideo(videos.length - 1);
}

window.onload = () => {
    fetchVideos();
};
