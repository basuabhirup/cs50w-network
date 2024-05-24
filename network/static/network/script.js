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
      window.location.pathname = "/posts"
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
  const button = event.target.closest(".edit-button");
  const postId = button.dataset.postId;
  const postElement = document.getElementById(`post-content-${postId}`);
  const postContent = new String(postElement.textContent);
  const likeButton = document.querySelector(`button[data-post-id="${postId}"].like-button`)
  const editButton = document.querySelector(`button[data-post-id="${postId}"].edit-button`)
  const likeCountsElement = document.querySelector(`#like-count-${postId}`)

  postElement.innerHTML = `
  <form id="edit-post-${postId}">
  <textarea id="new-content-${postId}" name="content" class="d-block w-100 mb-3" rows="3">${postContent}</textarea>
  <button class="btn btn-sm btn-primary" type='submit'>Save</button>
  <button class="btn btn-sm btn-outline-secondary" type="reset">Cancel</button>
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

    fetch(`/posts/${postId}`, {
      method: "PUT",
      body: JSON.stringify({
        "new_content": newContent,
      }),
    })
    .then((res) => res.json().then((json) => {
      if (res.status === 200) {
        postElement.innerHTML = ''
        postElement.textContent = newContent
        likeButton.style.display = "inline-block"
        editButton.style.display = "inline-block"
        likeCountsElement.style.display = "block"
        console.log(json.message)
      } else {
        alert(json.error)
      }
    }))
    .catch((err) => {
      console.error(err)
    })
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
  const button = event.target.closest(".like-button");
  const postId = button.dataset.postId;
  const likeCount = document.getElementById(`like-count-${postId}`);
  console.log(postId, button.innerHTML.trim())

  fetch(`/like/${postId}`).then((res) => {
    if (res.status === 200) {
      res.text().then((text) => {
        if (!button.innerHTML.trim().includes("bi-heart-fill")) {
          button.innerHTML = `<i class="bi bi-heart-fill text-danger"></i>`;
          likeCount.textContent = text;
        } else {
          button.innerHTML = `<i class="bi bi-heart text-danger"></i>`;
          likeCount.textContent = text;
        }
      });
    }
  });
};
