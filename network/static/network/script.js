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

const onPostEdit = (event) => {
  const button = event.target;
  const postId = button.dataset.postId;
  const postElement = document.getElementById(`post-content-${postId}`);
  const postContent = new String(postElement.textContent);
  const likeButton = document.querySelector(`button[data-post-id="${postId}"].like-button`)
  const editButton = document.querySelector(`button[data-post-id="${postId}"].edit-button`)
  const likeCountsElement = document.querySelector(`#like-count-${postId}`)

  postElement.innerHTML = `
  <form id="edit-post-${postId}">
  <textarea id="new-content-${postId}" name="content" rows="5" cols="50">${postContent}</textarea>
  <button type='submit'>Save</button>
  <button type="reset">Cancel</button>
  </form>
  `;

  likeButton.style.display = "none"
  editButton.style.display = "none"
  likeCountsElement.style.display = "none"

  const editForm = document.getElementById(`edit-post-${postId}`);

  editForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const newContent = document.getElementById(`new-content-${postId}`).value;
    console.log(newContent, postId);
  });

  editForm.addEventListener("reset", (event) => {
    event.preventDefault()
    postElement.innerHTML = postContent
    likeButton.style.display = "inline-block"
    editButton.style.display = "inline-block"
    likeCountsElement.style.display = "block"
  })
};

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
