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
  fetch(`/follow/${username}`, {
    method: "POST",
    body: JSON.stringify({
      follow,
    }),
  }).then((res) => {
    if (res.status === 200) {
      res.json().then((json) => {
        if (!!document.querySelector("button[name='follow']")) {
          // Change followers count without refreshing the page
          document.querySelector("#followers").textContent =
            "Followers: " + json.followers_count;

          // Toggle the follow button into unfollow
          document.querySelector("button[name='follow']").textContent =
            "Unfollow";
          document.querySelector("button[name='follow']").name = "unfollow";
        } else {
          // Change followers count without refreshing the page
          document.querySelector("#followers").textContent =
            "Followers: " + json.followers_count;

          // Toggle the unfollow button into follow
          document.querySelector("button[name='unfollow']").textContent =
            "Follow";
          document.querySelector("button[name='unfollow']").name = "follow";
        }
      });
    }
  });
};

// onPostEdit

const handleLiking = (event) => {
  const button = event.target;
  const postId = button.dataset.postId;
  const likeCount = document.getElementById(`like-count-${postId}`);

  fetch(`/like/${postId}`).then((res) => {
    if (res.status === 200) {
      res.text().then((text) => {
        if (button.textContent.trim() === "Like") {
          button.textContent = "Unlike";
          likeCount.textContent = "Likes: " + text;
        } else {
          button.textContent = "Like";
          likeCount.textContent = "Likes: " + text;
        }
      });
    }
  });
};
