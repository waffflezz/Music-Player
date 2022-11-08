function add_playlist(url, playlist_name) {
    let httpRequest = new XMLHttpRequest();

    function isBlank(str) {
        return (!str || /^\s*$/.test(str));
    }

    let error_string = document.getElementById('error_string');
    if (isBlank(playlist_name)) {
        error_string.style.color = "red";
        error_string.innerText = "String is empty!";
    } else {
        error_string.style.color = "green";
        error_string.innerText = "Playlist save!";
        httpRequest.open('GET', url + `?playlist_name=${playlist_name}`, true);
        httpRequest.send(null);
    }
}

function swap(url, direction, song_id) {
    let httpRequest = new XMLHttpRequest();
    if (direction === 'up') {
        httpRequest.open('GET', url + `?direction=${direction}&song_id=${song_id}`, true);
    } else if (direction === 'down') {
        httpRequest.open('GET', url + `?direction=${direction}&song_id=${song_id}`, true);
    }

    httpRequest.send(null);
}

function delete_playlist(url, playlist_id) {
    let httpRequest = new XMLHttpRequest();

    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                player.pause();
                player.src = "";
                document.getElementById("pills-playlists").innerHTML = httpRequest.responseText;
            } else {
                alert('С запросом возникла проблема.');
            }
        }
    };

    httpRequest.open('GET', url + `?playlist_id=${playlist_id}`, true);
    httpRequest.send(null);
}

function add_song_to_playlist(url, song_id, playlist_id) {
    let httpRequest = new XMLHttpRequest();

    httpRequest.open('GET', url + `?song_id=${song_id}&playlist_id=${playlist_id}`, true);
    httpRequest.send(null);
}

function delete_song_from_playlist(url, song_id, playlist_id) {
    let httpRequest = new XMLHttpRequest();

    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                update_songs_number();
                // document.getElementById("offcanvas-songs").innerHTML = httpRequest.responseText;
                player.src = "";
            } else {
                alert('С запросом возникла проблема.');
            }
        }
    };

    httpRequest.open('GET', url + `?song_id=${song_id}&playlist_id=${playlist_id}`, true);
    httpRequest.send(null);
}

function open_playlist(url, id) {
    let httpRequest = new XMLHttpRequest();
    pl_id = id;

    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                document.getElementById("offcanvas-songs").innerHTML = httpRequest.responseText;
                update_songs_number();
                if (current_pl_id == pl_id) {
                    change_current_item(player.getAttribute("data-song"));
                }
            } else {
                alert('С запросом возникла проблема.');
            }
        }
    };

    httpRequest.open('GET', url + `?pl_id=${id}`, true);
    httpRequest.send(null);
}

function update_playlists(url) {
    let httpRequest = new XMLHttpRequest();

    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                document.getElementById("pills-playlists").innerHTML = httpRequest.responseText;
            } else {
                alert('С запросом возникла проблема.');
            }
        }
    };

    httpRequest.open('GET', url, true);
    httpRequest.send(null);
}

function update_all_songs(url) {
    let httpRequest = new XMLHttpRequest();

    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                document.getElementById("pills-songs").innerHTML = httpRequest.responseText;
            } else {
                alert('С запросом возникла проблема.');
            }
        }
    };

    httpRequest.open('GET', url, true);
    httpRequest.send(null);
}

let player, pl_id, current_pl_id;

window.onload = () => {
    player = document.getElementById('main-player');

    player.addEventListener('ended', next_song);

    update_all_songs('all_songs');
};

function stop_play() {
    player.currentTime = 0;
    player.pause();
}

function next_song() {
    if (current_pl_id != pl_id) {
        return;
    }
    let httpRequest = new XMLHttpRequest();
    httpRequest.responseType = "json";

    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                if (pl_songs_len() === 0) {
                    return;
                }

                stop_play();
                let jsonResponse = httpRequest.response;
                player.src = jsonResponse['song_path'];
                player.play();
                let song_id = Number(player.getAttribute("data-song"));

                player.setAttribute("data-song", song_id + 1 >= pl_songs_len() ? 0 : song_id + 1);
                change_current_item(player.getAttribute("data-song"));
                changeImage(jsonResponse['image']);
                // } else {
                //     alert('С запросом возникла проблема.');
            }
        }
    };

    httpRequest.open('GET', 'next_song', true);
    httpRequest.send(null);
}

function prev_song() {
    if (current_pl_id != pl_id) {
        return;
    }
    let httpRequest = new XMLHttpRequest();
    httpRequest.responseType = "json";

    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                if (pl_songs_len() === 0) {
                    return;
                }
                stop_play();

                let jsonResponse = httpRequest.response;
                player.src = jsonResponse['song_path'];
                player.play();
                let song_id = Number(player.getAttribute("data-song"));

                player.setAttribute("data-song", song_id - 1 < 0 ? pl_songs_len() - 1 : song_id - 1);
                change_current_item(player.getAttribute("data-song"));
                changeImage(jsonResponse['image']);
                // } else {
                //     alert('С запросом возникла проблема.');
            }
        }
    };

    httpRequest.open('GET', 'prev_song', true);
    httpRequest.send(null);
}

const changeImage = (image) => {
    document.getElementById('title_image').src = "data:image/png;base64," + image;
    // document.getElementById('title_image').src = image;
};

const formatTime = (time) => {
    let min = Math.floor(time / 60);
    if (min < 10) {
        min = `0` + min;
    }

    let sec = Math.floor(time % 60);
    if (sec < 10) {
        sec = `0` + sec;
    }

    return `${min} : ${sec}`;
};

function resume_song_color() {
    for (let i = 0; i < pl_songs_len(); i++) {
        document.getElementById("all-songs").children[i].style.background = "aquamarine";
    }
}

function resume_swap_elements() {
    for (let i = 0; i < pl_songs_len(); i++) {
        if (document.getElementsByClassName("swap_item").length === 0) {
            return;
        }
        document.getElementsByClassName("swap_item")[0].remove();
    }
}

function update_songs_number() {
    for (let i = 0; i < pl_songs_len(); i++) {
        document.getElementById("all-songs").children[i].setAttribute("data-song", `${i}`);
    }
}

function pl_songs_len() {
    return document.getElementById("all-songs").children.length;
}

function change_current_color(data) {
    resume_song_color();
    document.getElementById("all-songs").children[data].style.background = "aqua";
}

function change_current_item(data) {
    change_current_color(data)
    resume_swap_elements();

    let swap_up = document.createElement('div');
    swap_up.className = "swap_item";
    swap_up.innerText = "up";
    swap_up.onclick = function () {
        swap('swap', 'up', data);
        open_playlist('open_playlist', pl_id);
    };
    let swap_down = document.createElement('div');
    swap_down.className = "swap_item";
    swap_down.innerText = "down"
    swap_down.onclick = function () {
        swap('swap', 'down', data);
        open_playlist('open_playlist', pl_id);
    };

    document.getElementById("all-songs").children[data].appendChild(swap_up);
    document.getElementById("all-songs").children[data].appendChild(swap_down);
}

function play_song(url, data) {
    let httpRequest = new XMLHttpRequest();
    httpRequest.responseType = "json";

    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                stop_play();

                let jsonResponse = httpRequest.response;
                player.src = jsonResponse['song_path'];
                player.play();
                changeImage(jsonResponse['image']);

                let seekBar = document.getElementById("seek-bar");
                let seekBarLabel = document.getElementById("seek-bar-label");

                player.onloadedmetadata = () => {
                    seekBar.max = player.duration;
                };

                setInterval(() => {
                    seekBar.value = player.currentTime;
                    seekBarLabel.innerText = `${formatTime(player.currentTime)} ----- ${formatTime(player.duration)}`
                }, 500);

                seekBar.addEventListener('change', () => {
                    player.currentTime = seekBar.value;
                });

                player.setAttribute("data-song", data);

                current_pl_id = jsonResponse['playlist_id'];
                change_current_item(data);

            } else {
                alert('С запросом возникла проблема.');
            }
        }
    };

    httpRequest.open('GET', url + `?song_number=${data}&pl_id=${pl_id}`, true);
    httpRequest.send(null);
}

function continue_play_song() {
    if (player.src !== "") {
        player.play();
    }
}

function pause_song() {
    if (player.src !== "") {
        player.pause();
    }
}
