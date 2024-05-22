let newPostForm;
let newPost;

document.addEventListener("DOMContentLoaded", () => {
  newPostForm = document.querySelector("#new-post-form");
  newPostContent = document.querySelector("#new-post");
});

const onNewPost = (e) => {
  e.preventDefault();
  console.log(newPostContent.value);
  // API Call
  fetch("/posts", {
    method: "POST",
    body: JSON.stringify({
      content: newPostContent.value,
    }),
  }).then((res) => {
    if (res.status === 201) {
      newPostContent.value = "";
    }
  });
};

const handleFollowing = (event) => {
  const follow = event.target.name === "follow";
  const username = window.location.pathname.split("/")[2];
  // console.log(username, follow);
  fetch(`/follow/${username}`, {
    method: "POST",
    body: JSON.stringify({
      username,
      follow,
    }),
  }).then((res) => {
    if (res.status === 200) {
      if (!!document.querySelector("button[name='follow']")) {
        // Change followers count without refreshing the page
        document.querySelector("#followers").textContent =
          document.querySelector("#followers").textContent.split(": ")[0] +
          ": " +
          (parseInt(
            document.querySelector("#followers").textContent.split(": ")[1]
          ) +
            parseInt(1));

        // Toggle the follow button into unfollow
        document.querySelector("button[name='follow']").textContent =
          "Unfollow";
        document.querySelector("button[name='follow']").name = "unfollow";
      } else {
        // Change followers count without refreshing the page
        document.querySelector("#followers").textContent =
          document.querySelector("#followers").textContent.split(": ")[0] +
          ": " +
          (parseInt(
            document.querySelector("#followers").textContent.split(": ")[1]
          ) -
            parseInt(1));

        // Toggle the unfollow button into follow
        document.querySelector("button[name='unfollow']").textContent =
          "Follow";
        document.querySelector("button[name='unfollow']").name = "follow";
      }
    }
  });
};

// onPostEdit

// handleLiking
